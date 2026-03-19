"""
WalkingPad BLE Protocol
=======================
Protocollo binario per comunicare con tapis roulant KingSmith WalkingPad via BLE GATT.

Basato sul reverse engineering indipendente di:
  - ph4r05/ph4-walkingpad (Python, MIT) — via ADB logcat dell'app ufficiale
  - DorianRudolph/QWalkingPad (C++, GPL3) — reverse engineering indipendente

Formato pacchetto:
  [0xF7] [command_type] [payload...] [checksum] [0xFD]
  checksum = sum(bytes[1:-2]) % 256

Questo modulo definisce:
  - Costanti UUID e comandi
  - Funzioni per costruire pacchetti di comando
  - Parser per le risposte del dispositivo
"""

from dataclasses import dataclass, field
from typing import Optional

# ── UUID GATT ────────────────────────────────────────────────
SERVICE_UUID = "0000fe00-0000-1000-8000-00805f9b34fb"
NOTIFY_CHAR  = "0000fe01-0000-1000-8000-00805f9b34fb"  # device → host
WRITE_CHAR   = "0000fe02-0000-1000-8000-00805f9b34fb"  # host → device

# ── Costanti pacchetto ───────────────────────────────────────
HEADER = 0xF7
FOOTER = 0xFD
RESP_HEADER = bytes([0xF8, 0xA2])

# ── Tipi comando ─────────────────────────────────────────────
CMD_BYTE = 0xA2    # comandi brevi (6 byte)
CMD_INT  = 0xA6    # comandi con valore intero (9 byte)
CMD_SYNC = 0xA7    # sincronizzazione record

# ── Chiavi comando byte (CMD_BYTE) ──────────────────────────
KEY_QUERY_STATUS = 0x00
KEY_SET_SPEED    = 0x01
KEY_SET_MODE     = 0x02
KEY_START_BELT   = 0x04

# ── Chiavi comando intero (CMD_INT) ──────────────────────────
KEY_QUERY_PARAMS   = 0x00
KEY_SET_MAX_SPEED   = 0x03
KEY_SET_START_SPEED = 0x04
KEY_SET_SENSITIVITY = 0x06

# ── Modalità nastro ─────────────────────────────────────────
MODE_AUTO    = 0
MODE_MANUAL  = 1
MODE_STANDBY = 2

# ── Stato nastro ────────────────────────────────────────────
BELT_STOPPED  = 0
BELT_RUNNING  = 1
BELT_STANDBY  = 5   # lock mode — richiede unlock
# Countdown avvio (osservati dal test reale 2026-03-19):
BELT_COUNTDOWN_3 = 9   # 3 secondi all'avvio
BELT_COUNTDOWN_2 = 8   # 2 secondi
BELT_COUNTDOWN_1 = 7   # 1 secondo
BELT_STARTING    = 3   # decelerazione/arresto in corso

# ── Pacchetti pre-costruiti ──────────────────────────────────
# NoOp / query status — funge anche da keep-alive
CMD_NOOP = bytes([0xF7, 0xA2, 0x00, 0x00, 0xA2, 0xFD])

# Unlock (quando il nastro è in lock mode, belt_state == 5)
CMD_UNLOCK = bytes([0xF7, 0xA2, 0x02, 0x01, 0xA5, 0xFD])

# Query parametri configurazione
CMD_QUERY_PARAMS = bytes([0xF7, 0xA6, 0x00, 0x00, 0x00, 0x00, 0x00, 0xA6, 0xFD])

# ── Handshake iniziale (dall'app ufficiale KingSmith) ────────
# Profile payload — inviato come primo comando dopo la connessione BLE.
# Payload opaco hardcoded dall'app ufficiale (profilo 0), probabilmente
# serve come autenticazione/inizializzazione del dispositivo.
CMD_PROFILE = bytes([0xF7, 0xA5, 0x60, 0x4A, 0x4D, 0x93, 0x71, 0x29, 0xC9, 0xFD])

# Beep + status request — conferma che il dispositivo è vivo e risponde.
CMD_BEEP = bytes([0xF7, 0xA2, 0x03, 0x07, 0xAC, 0xFD])


# ── Costruzione pacchetti ────────────────────────────────────

def _checksum(payload: bytes) -> int:
    """Calcola checksum: somma dei byte del payload modulo 256."""
    return sum(payload) % 256


def build_byte_cmd(key: int, value: int) -> bytes:
    """Costruisce un comando breve (6 byte).

    Formato: [0xF7, 0xA2, key, value, checksum, 0xFD]
    """
    payload = bytes([CMD_BYTE, key, value])
    return bytes([HEADER]) + payload + bytes([_checksum(payload), FOOTER])


def build_int_cmd(key: int, value: int) -> bytes:
    """Costruisce un comando con valore intero a 3 byte big-endian (9 byte totali).

    Formato: [0xF7, 0xA6, key, 0x00, b2, b1, b0, checksum, 0xFD]
    """
    b2 = (value >> 16) & 0xFF
    b1 = (value >> 8) & 0xFF
    b0 = value & 0xFF
    payload = bytes([CMD_INT, key, 0x00, b2, b1, b0])
    return bytes([HEADER]) + payload + bytes([_checksum(payload), FOOTER])


def cmd_set_speed(speed_units: int) -> bytes:
    """Imposta velocità nastro. speed_units in decimi di km/h (es. 15 = 1.5 km/h)."""
    return build_byte_cmd(KEY_SET_SPEED, speed_units)


def cmd_set_mode(mode: int) -> bytes:
    """Imposta modalità: MODE_AUTO (0), MODE_MANUAL (1), MODE_STANDBY (2)."""
    return build_byte_cmd(KEY_SET_MODE, mode)


def cmd_start_belt() -> bytes:
    """Avvia il nastro."""
    return build_byte_cmd(KEY_START_BELT, 0x01)


def cmd_set_max_speed(speed_units: int) -> bytes:
    """Imposta velocità massima. speed_units in decimi di km/h."""
    return build_int_cmd(KEY_SET_MAX_SPEED, speed_units)


def cmd_set_start_speed(speed_units: int) -> bytes:
    """Imposta velocità di partenza. speed_units in decimi di km/h."""
    return build_int_cmd(KEY_SET_START_SPEED, speed_units)


def cmd_set_sensitivity(level: int) -> bytes:
    """Imposta sensibilità sensore: 1=alta, 2=media, 3=bassa."""
    return build_int_cmd(KEY_SET_SENSITIVITY, level)


# ── Struttura dati risposta ──────────────────────────────────

@dataclass
class WalkingPadStatus:
    """Stato corrente del WalkingPad, parsato da un pacchetto di risposta."""
    belt_state: int = 0          # 0=fermo, 1=in moto, 5=locked
    speed: int = 0               # velocità raw (decimi di km/h)
    manual_mode: int = 0         # 0=auto, 1=manuale
    time_s: int = 0              # tempo sessione in secondi
    dist_raw: int = 0            # distanza raw (centesimi di km)
    steps: int = 0               # conteggio passi
    app_speed: int = 0           # velocità target dal sensore piede
    controller_button: int = 0   # stato pulsante fisico
    raw: Optional[bytes] = field(default=None, repr=False)

    @property
    def speed_kmh(self) -> float:
        """Velocità in km/h."""
        return self.speed * 0.1

    @property
    def dist_m(self) -> float:
        """Distanza in metri."""
        return self.dist_raw * 10

    @property
    def is_running(self) -> bool:
        return self.belt_state == BELT_RUNNING

    @property
    def is_locked(self) -> bool:
        return self.belt_state == BELT_STANDBY


def _bytes_to_int(data: bytes, offset: int) -> int:
    """Decodifica 3 byte big-endian in intero."""
    return (data[offset] << 16) | (data[offset + 1] << 8) | data[offset + 2]


def parse_status(data: bytes) -> Optional[WalkingPadStatus]:
    """Parsa un pacchetto di stato dal WalkingPad.

    Ritorna None se il pacchetto non è valido o non è un pacchetto di stato.

    Formato risposta stato (20 byte, header 0xF8 0xA2):
        byte[2]     belt_state
        byte[3]     speed (x0.1 km/h)
        byte[4]     manual_mode
        byte[5:8]   time (3 byte big-endian, secondi)
        byte[8:11]  distance (3 byte big-endian, centesimi di km)
        byte[11:14] steps (3 byte big-endian)
        byte[14]    app_speed (velocità sensore piede)
        byte[16]    controller_button
    """
    # Validazione lunghezza — qdomyos-zwift ignora pacchetti != 20 byte
    if len(data) < 17:
        return None

    # Verifica header risposta stato
    if data[0:2] != RESP_HEADER:
        return None

    # Verifica checksum (se il pacchetto è completo)
    if len(data) >= 20:
        expected_cs = _checksum(data[1:-2])
        actual_cs = data[-2]
        if expected_cs != actual_cs:
            return None

    return WalkingPadStatus(
        belt_state=data[2],
        speed=data[3],
        manual_mode=data[4],
        time_s=_bytes_to_int(data, 5),
        dist_raw=_bytes_to_int(data, 8),
        steps=_bytes_to_int(data, 11),
        app_speed=data[14] if len(data) > 14 else 0,
        controller_button=data[16] if len(data) > 16 else 0,
        raw=bytes(data),
    )
