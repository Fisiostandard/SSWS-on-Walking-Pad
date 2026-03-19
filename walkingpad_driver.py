"""
WalkingPad BLE Driver
=====================
Driver Bluetooth Low Energy per tapis roulant KingSmith WalkingPad.
Comunicazione diretta via bleak, senza dipendenze da librerie terze non mantenute.

Funzionalità:
  - Connessione BLE con auto-reconnect
  - Coda comandi con throttling (evita di sovraccaricare il device)
  - Keep-alive automatico (polling stato ogni 200ms)
  - Validazione pacchetti e ignore first packet
  - Rilevamento lock mode con auto-unlock
  - Grace period su start/stop per evitare falsi trigger
  - Callback per aggiornamenti di stato in tempo reale

Uso:
    driver = WalkingPadDriver(address="XX:XX:XX:XX:XX:XX")
    driver.on_status = my_callback
    await driver.connect()
    await driver.start_belt()
    await driver.set_speed(15)  # 1.5 km/h
    ...
    await driver.stop_belt()
    await driver.disconnect()
"""

import asyncio
import logging
import time
from collections import deque
from typing import Callable, Optional

from bleak import BleakClient, BleakScanner
from bleak.exc import BleakError

from walkingpad_protocol import (
    SERVICE_UUID,
    NOTIFY_CHAR,
    WRITE_CHAR,
    BELT_STANDBY,
    CMD_NOOP,
    CMD_UNLOCK,
    CMD_QUERY_PARAMS,
    CMD_PROFILE,
    CMD_BEEP,
    WalkingPadStatus,
    cmd_set_speed,
    cmd_set_mode,
    cmd_start_belt,
    cmd_set_max_speed,
    cmd_set_start_speed,
    cmd_set_sensitivity,
    parse_status,
    MODE_MANUAL,
    MODE_STANDBY,
)

log = logging.getLogger("walkingpad")

# ── Configurazione timing ────────────────────────────────────
POLL_INTERVAL_S     = 0.2     # 200ms — keep-alive e polling stato
CMD_MIN_INTERVAL_S  = 0.1     # 100ms minimo tra comandi (QWalkingPad usa 50ms, ph4 690ms)
WRITE_TIMEOUT_S     = 0.3     # 300ms timeout per risposta dopo write (da qdomyos-zwift)
RECONNECT_DELAY_S   = 2.0     # attesa prima di tentare riconnessione
MAX_RECONNECT       = 5       # tentativi massimi di riconnessione
GRACE_AFTER_START_S = 10.0    # grace period dopo start (da qdomyos-zwift)
GRACE_AFTER_STOP_S  = 3.0     # grace period dopo stop


class WalkingPadDriver:
    """Driver BLE per WalkingPad con gestione robusta della connessione."""

    def __init__(self, address: str):
        """
        Args:
            address: Indirizzo BLE del WalkingPad.
                     Su macOS è un UUID (es. "D455A571-F8BB-6D26-92BF-087B9BA73ABF").
                     Su Linux/Windows è un MAC (es. "AA:BB:CC:DD:EE:FF").
        """
        self.address = address

        # ── Callback ────────────────────────────────────────
        self.on_status: Optional[Callable[[WalkingPadStatus], None]] = None
        self.on_disconnect: Optional[Callable[[], None]] = None
        self.on_tamper: Optional[Callable[[str], None]] = None  # telecomando/manomissione

        # ── Stato interno ───────────────────────────────────
        self._client: Optional[BleakClient] = None
        self._connected = False
        self._running = False              # loop principale attivo
        self._ignore_next_packet = True    # ignora primo pacchetto (dati stale)
        self._last_cmd_time = 0.0          # timestamp ultimo comando inviato
        self._last_status: Optional[WalkingPadStatus] = None
        self._start_time: Optional[float] = None  # timestamp avvio nastro
        self._stop_time: Optional[float] = None    # timestamp stop nastro
        self._reconnect_count = 0
        self._cmd_queue: asyncio.Queue = asyncio.Queue()
        self._response_event: asyncio.Event = asyncio.Event()
        self._poll_task: Optional[asyncio.Task] = None
        self._cmd_task: Optional[asyncio.Task] = None
        self._expected_mode: Optional[int] = None  # modo impostato dal software
        self._last_set_speed: Optional[int] = None  # ultima velocità comandata da noi

        self._prev_belt_state: Optional[int] = None  # per distinguere stop telecomando vs step-off

        # ── Speed history buffer (da CodeJawn) ──────────────
        self.speed_history: deque = deque(maxlen=15)

    # ── Proprietà pubbliche ──────────────────────────────────

    @property
    def connected(self) -> bool:
        return self._connected

    @property
    def last_status(self) -> Optional[WalkingPadStatus]:
        return self._last_status

    @property
    def in_grace_after_start(self) -> bool:
        if self._start_time is None:
            return False
        return (time.time() - self._start_time) < GRACE_AFTER_START_S

    @property
    def in_grace_after_stop(self) -> bool:
        if self._stop_time is None:
            return False
        return (time.time() - self._stop_time) < GRACE_AFTER_STOP_S

    # ── Connessione ──────────────────────────────────────────

    async def connect(self) -> bool:
        """Connette al WalkingPad. Ritorna True se la connessione ha successo."""
        log.info("Connessione a %s...", self.address)

        try:
            self._client = BleakClient(
                self.address,
                disconnected_callback=self._on_ble_disconnect,
            )
            await self._client.connect(timeout=10.0)

            # Verifica che il servizio WalkingPad sia presente
            services = self._client.services
            if not services.get_service(SERVICE_UUID):
                log.error("Servizio WalkingPad (FE00) non trovato sul dispositivo")
                await self._client.disconnect()
                return False

            # Verifica che le caratteristiche esistano
            notify_char = services.get_characteristic(NOTIFY_CHAR)
            write_char = services.get_characteristic(WRITE_CHAR)
            if not notify_char or not write_char:
                log.error("Caratteristiche BLE (FE01/FE02) non trovate")
                await self._client.disconnect()
                return False

            # Attiva notifiche
            await self._client.start_notify(NOTIFY_CHAR, self._on_notification)

            self._connected = True
            self._ignore_next_packet = True
            self._reconnect_count = 0
            self._running = True

            # Avvia loop polling e coda comandi
            self._poll_task = asyncio.create_task(self._poll_loop())
            self._cmd_task = asyncio.create_task(self._cmd_processor())

            # Handshake iniziale (stessa sequenza dell'app ufficiale KingSmith)
            # 1. Profile payload — autenticazione/inizializzazione dispositivo
            await self._enqueue(CMD_PROFILE)
            await asyncio.sleep(1.5)
            # 2. Beep + status request — conferma che il device risponde
            await self._enqueue(CMD_BEEP)
            await asyncio.sleep(1.0)
            # 3. Query parametri configurazione
            await self._enqueue(CMD_QUERY_PARAMS)

            log.info("Connesso a WalkingPad %s", self.address)
            return True

        except (BleakError, asyncio.TimeoutError, OSError) as e:
            log.error("Errore connessione: %s", e)
            self._connected = False
            return False

    async def disconnect(self):
        """Disconnette dal WalkingPad in modo pulito."""
        log.info("Disconnessione...")
        self._running = False

        # Ferma i task
        if self._poll_task and not self._poll_task.done():
            self._poll_task.cancel()
            try:
                await self._poll_task
            except asyncio.CancelledError:
                pass

        if self._cmd_task and not self._cmd_task.done():
            self._cmd_task.cancel()
            try:
                await self._cmd_task
            except asyncio.CancelledError:
                pass

        # Disconnetti BLE
        if self._client and self._client.is_connected:
            try:
                await self._client.stop_notify(NOTIFY_CHAR)
            except Exception:
                pass
            try:
                await self._client.disconnect()
            except Exception:
                pass

        self._connected = False
        log.info("Disconnesso")

    async def _reconnect(self):
        """Tenta la riconnessione automatica dopo una disconnessione."""
        if self._reconnect_count >= MAX_RECONNECT:
            log.error("Raggiunto limite riconnessioni (%d). Arresto.", MAX_RECONNECT)
            self._running = False
            return

        self._reconnect_count += 1
        log.warning(
            "Tentativo riconnessione %d/%d in %.1fs...",
            self._reconnect_count, MAX_RECONNECT, RECONNECT_DELAY_S,
        )
        await asyncio.sleep(RECONNECT_DELAY_S)

        # Pulizia client precedente
        if self._client:
            try:
                await self._client.disconnect()
            except Exception:
                pass

        success = await self.connect()
        if not success:
            log.warning("Riconnessione fallita")

    # ── Callback BLE ─────────────────────────────────────────

    def _on_ble_disconnect(self, client: BleakClient):
        """Callback chiamato da bleak quando la connessione BLE cade."""
        log.warning("Connessione BLE persa")
        self._connected = False

        if self.on_disconnect:
            self.on_disconnect()

        # Schedula riconnessione se il driver è ancora attivo
        if self._running:
            asyncio.get_event_loop().create_task(self._reconnect())

    def _on_notification(self, sender, data: bytearray):
        """Callback per ogni notifica ricevuta dal WalkingPad."""
        # Ignora primo pacchetto dopo connessione (dati stale, da qdomyos-zwift)
        if self._ignore_next_packet:
            self._ignore_next_packet = False
            log.debug("Primo pacchetto ignorato (stale data)")
            return

        # Segnala che abbiamo ricevuto una risposta (per il timeout write)
        self._response_event.set()

        # Parsa il pacchetto
        status = parse_status(bytes(data))
        if status is None:
            log.debug("Pacchetto non valido o non di stato (%d byte): %s",
                       len(data), data.hex())
            return

        self._last_status = status

        # Speed history buffer (da CodeJawn)
        self.speed_history.append(status.speed_kmh)

        # Auto-unlock se in lock mode
        if status.is_locked:
            log.info("Lock mode rilevato, invio unlock...")
            asyncio.get_event_loop().create_task(self._enqueue(CMD_UNLOCK))

        # ── Rilevamento manomissione telecomando ─────────
        # Disattivo durante le fasi di transizione (grace period)
        tamper_active = (
            not self.in_grace_after_start
            and not self.in_grace_after_stop
            and self._start_time is not None   # sessione avviata
        )

        if not tamper_active:
            pass

        # STOP non comandato: il nastro si è fermato ma noi non abbiamo
        # dato il comando di stop.
        # Distinguiamo due casi:
        #   - belt_state passa da 1 direttamente a 0/5 → telecomando STOP (brusco)
        #   - belt_state passa per 3 (decelerazione) → paziente sceso dal nastro
        elif status.belt_state in (0, BELT_STANDBY) and self._stop_time is None:
            if self._prev_belt_state == 1:
                # Salto diretto da "in moto" a "fermo" → telecomando
                msg = "TAMPER: nastro fermato dal telecomando!"
                log.warning(msg)
                if self.on_tamper:
                    self.on_tamper(msg)
            elif self._prev_belt_state == 3:
                # Passato per decelerazione → paziente sceso
                msg = "STEP-OFF: paziente sceso dal nastro (decelerazione naturale)"
                log.info(msg)
                if self.on_tamper:
                    self.on_tamper(msg)
            else:
                # Caso ambiguo (es. primo pacchetto dopo connessione)
                msg = "STOP non comandato (causa incerta)"
                log.warning(msg)
                if self.on_tamper:
                    self.on_tamper(msg)

        # Decelerazione in corso non comandata — il paziente sta scendendo
        # (loggo ma non allarmo ancora, aspetto belt_state 0 per confermare)
        elif status.belt_state == 3 and self._stop_time is None:
            log.debug("Decelerazione non comandata in corso (belt_state=3)")

        # Cambio modo non comandato
        elif (status.belt_state == 1
                and self._expected_mode is not None
                and status.manual_mode != self._expected_mode):
            msg = (f"TAMPER: modo cambiato da telecomando "
                   f"(atteso={self._expected_mode}, rilevato={status.manual_mode})")
            log.warning(msg)
            if self.on_tamper:
                self.on_tamper(msg)
            asyncio.get_event_loop().create_task(
                self._enqueue(cmd_set_mode(self._expected_mode)))

        # Velocità modificata da telecomando (+/-)
        elif (status.belt_state == 1
                and self._last_set_speed is not None
                and status.speed > 0
                and abs(status.speed - self._last_set_speed) > 5):
            msg = (f"TAMPER: velocità modificata da telecomando "
                   f"(comandata={self._last_set_speed}, rilevata={status.speed})")
            log.warning(msg)
            if self.on_tamper:
                self.on_tamper(msg)

        # Loggo controller_button per capire se il telecomando manda un segnale
        # distinguibile (da verificare col test fisico)
        if status.controller_button != 0:
            log.info("controller_button=%d (belt=%d speed=%d)",
                     status.controller_button, status.belt_state, status.speed)

        # Aggiorna stato precedente per la prossima iterazione
        self._prev_belt_state = status.belt_state

        # Callback utente
        if self.on_status:
            try:
                self.on_status(status)
            except Exception as e:
                log.error("Errore nel callback on_status: %s", e)

    # ── Coda comandi con throttling ──────────────────────────

    async def _enqueue(self, cmd: bytes):
        """Aggiunge un comando alla coda."""
        await self._cmd_queue.put(cmd)

    async def _cmd_processor(self):
        """Processa la coda comandi rispettando il timing minimo tra invii."""
        while self._running:
            try:
                cmd = await asyncio.wait_for(self._cmd_queue.get(), timeout=1.0)
            except asyncio.TimeoutError:
                continue
            except asyncio.CancelledError:
                return

            await self._write_cmd(cmd)

    async def _write_cmd(self, cmd: bytes):
        """Invia un comando BLE con throttling e timeout risposta.

        - Rispetta intervallo minimo tra comandi (CMD_MIN_INTERVAL_S)
        - Attende risposta o timeout (WRITE_TIMEOUT_S)
        """
        if not self._connected or not self._client or not self._client.is_connected:
            log.debug("Write ignorato: non connesso")
            return

        # Throttling: attendi se troppo presto
        elapsed = time.time() - self._last_cmd_time
        if elapsed < CMD_MIN_INTERVAL_S:
            await asyncio.sleep(CMD_MIN_INTERVAL_S - elapsed)

        # Resetta evento risposta
        self._response_event.clear()

        try:
            await self._client.write_gatt_char(WRITE_CHAR, cmd, response=False)
            self._last_cmd_time = time.time()
            log.debug("TX: %s", cmd.hex())
        except (BleakError, OSError) as e:
            log.warning("Errore write BLE: %s", e)
            return

        # Attendi risposta o timeout (da qdomyos-zwift: 300ms)
        try:
            await asyncio.wait_for(self._response_event.wait(), timeout=WRITE_TIMEOUT_S)
        except asyncio.TimeoutError:
            log.debug("Timeout risposta per comando %s", cmd.hex())

    # ── Polling loop (keep-alive) ────────────────────────────

    async def _poll_loop(self):
        """Loop di polling: invia NoOp ogni POLL_INTERVAL_S per mantenere
        la connessione e ricevere aggiornamenti di stato."""
        while self._running:
            try:
                if self._connected:
                    await self._write_cmd(CMD_NOOP)
                await asyncio.sleep(POLL_INTERVAL_S)
            except asyncio.CancelledError:
                return
            except Exception as e:
                log.error("Errore nel poll loop: %s", e)
                await asyncio.sleep(1.0)

    # ── Comandi pubblici ─────────────────────────────────────

    async def start_belt(self):
        """Avvia il nastro."""
        log.info("Avvio nastro")
        self._start_time = time.time()
        self._stop_time = None
        await self._enqueue(cmd_start_belt())

    async def stop_belt(self):
        """Ferma il nastro impostando modalità standby."""
        log.info("Stop nastro")
        self._stop_time = time.time()
        self._start_time = None
        self._expected_mode = MODE_STANDBY  # aggiorna attesa per evitare falso tamper
        await self._enqueue(cmd_set_speed(0))
        await asyncio.sleep(0.2)
        await self._enqueue(cmd_set_mode(MODE_STANDBY))

    async def set_speed(self, speed_units: int):
        """Imposta velocità. speed_units in decimi di km/h (es. 15 = 1.5 km/h)."""
        speed_units = max(0, min(speed_units, 80))  # clamp 0-8.0 km/h
        self._last_set_speed = speed_units
        await self._enqueue(cmd_set_speed(speed_units))

    async def set_mode(self, mode: int):
        """Imposta modalità: MODE_AUTO=0, MODE_MANUAL=1, MODE_STANDBY=2."""
        self._expected_mode = mode
        await self._enqueue(cmd_set_mode(mode))

    async def set_max_speed(self, speed_units: int):
        """Imposta velocità massima. speed_units in decimi di km/h."""
        speed_units = max(10, min(speed_units, 80))  # clamp 1.0-8.0 km/h
        await self._enqueue(cmd_set_max_speed(speed_units))

    async def set_start_speed(self, speed_units: int):
        """Imposta velocità di partenza. speed_units in decimi di km/h."""
        speed_units = max(0, min(speed_units, 30))  # clamp 0-3.0 km/h
        await self._enqueue(cmd_set_start_speed(speed_units))

    async def set_sensitivity(self, level: int):
        """Imposta sensibilità sensore: 1=alta, 2=media, 3=bassa."""
        level = max(1, min(level, 3))
        await self._enqueue(cmd_set_sensitivity(level))

    async def set_manual_mode(self):
        """Imposta modalità manuale (velocità controllata dal software)."""
        self._expected_mode = MODE_MANUAL
        await self._enqueue(cmd_set_mode(MODE_MANUAL))

    # ── Utility ──────────────────────────────────────────────

    @staticmethod
    async def scan(timeout: float = 5.0) -> list:
        """Scansiona dispositivi BLE e ritorna quelli che sembrano WalkingPad.

        Ritorna lista di tuple (address, name).
        """
        log.info("Scansione BLE in corso (%ds)...", timeout)
        devices = await BleakScanner.discover(timeout=timeout)
        walkingpads = []
        for d in devices:
            name = d.name or ""
            if any(kw in name.upper() for kw in ["WALKINGPAD", "KINGSMITH", "KS-"]):
                walkingpads.append((d.address, d.name))
                log.info("  Trovato: %s (%s)", d.name, d.address)
        if not walkingpads:
            log.info("  Nessun WalkingPad trovato")
        return walkingpads
