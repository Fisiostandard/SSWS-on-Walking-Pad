#!/usr/bin/env python3
"""
WalkingPad Compatibility Check
==============================
Verifica se un tapis roulant BLE è compatibile con il driver WalkingPad SSWS.

Modalità SOLO LETTURA: non invia MAI comandi di movimento.
Sicuro da usare con qualsiasi dispositivo.

Uso:
    python walkingpad_compat_check.py                  # scansione + check automatico
    python walkingpad_compat_check.py AA:BB:CC:DD:EE   # check dispositivo specifico
"""

import asyncio
import logging
import sys
import time
from dataclasses import dataclass, field
from typing import Optional

from bleak import BleakClient, BleakScanner
from bleak.exc import BleakError

from walkingpad_protocol import (
    SERVICE_UUID,
    NOTIFY_CHAR,
    WRITE_CHAR,
    CMD_NOOP,
    CMD_PROFILE,
    CMD_QUERY_PARAMS,
    RESP_HEADER,
    parse_status,
)

log = logging.getLogger("compat_check")

# ── Risultato check ─────────────────────────────────────────────

CHECK_PASS = "PASS"
CHECK_FAIL = "FAIL"
CHECK_WARN = "WARN"
CHECK_SKIP = "SKIP"

SYMBOLS = {
    CHECK_PASS: "\u2705",  # green check
    CHECK_FAIL: "\u274c",  # red X
    CHECK_WARN: "\u26a0\ufe0f",   # warning
    CHECK_SKIP: "\u23ed\ufe0f",   # skip
}


@dataclass
class CheckResult:
    name: str
    status: str  # PASS, FAIL, WARN, SKIP
    detail: str = ""
    critical: bool = False  # se True, FAIL blocca il funzionamento


@dataclass
class CompatReport:
    device_name: str = ""
    device_address: str = ""
    checks: list = field(default_factory=list)

    @property
    def compatible(self) -> bool:
        """Compatibile se nessun check critico è FAIL."""
        return not any(c.status == CHECK_FAIL and c.critical for c in self.checks)

    @property
    def has_warnings(self) -> bool:
        return any(c.status == CHECK_WARN for c in self.checks)

    def add(self, name: str, status: str, detail: str = "", critical: bool = False):
        self.checks.append(CheckResult(name, status, detail, critical))

    def print_report(self):
        print("\n" + "=" * 60)
        print("  WALKINGPAD COMPATIBILITY REPORT")
        print("=" * 60)
        print(f"  Dispositivo : {self.device_name or 'N/A'}")
        print(f"  Indirizzo   : {self.device_address}")
        print("-" * 60)

        for c in self.checks:
            sym = SYMBOLS.get(c.status, "?")
            crit = " [CRITICO]" if c.critical and c.status == CHECK_FAIL else ""
            print(f"  {sym} {c.name}: {c.status}{crit}")
            if c.detail:
                for line in c.detail.split("\n"):
                    print(f"       {line}")

        print("-" * 60)
        if self.compatible:
            if self.has_warnings:
                print("  RISULTATO: COMPATIBILE (con avvertenze)")
                print("  Il driver dovrebbe funzionare, ma verifica le avvertenze.")
            else:
                print("  RISULTATO: COMPATIBILE")
                print("  Il driver dovrebbe funzionare senza modifiche.")
        else:
            print("  RISULTATO: NON COMPATIBILE")
            print("  Il driver NON funzionerà con questo dispositivo.")
            print("  Verifica i check marcati [CRITICO].")
        print("=" * 60 + "\n")


# ── Scanner ─────────────────────────────────────────────────────

KNOWN_PREFIXES = ["WALKINGPAD", "KINGSMITH", "KS-"]


async def scan_devices(timeout: float = 8.0) -> list:
    """Scansiona tutti i dispositivi BLE e li classifica."""
    print(f"\nScansione BLE in corso ({timeout}s)...")
    devices = await BleakScanner.discover(timeout=timeout)

    walkingpads = []
    other_ble = []

    for d in devices:
        name = d.name or ""
        if any(kw in name.upper() for kw in KNOWN_PREFIXES):
            walkingpads.append(d)
        elif name:
            other_ble.append(d)

    if walkingpads:
        print(f"\nDispositivi WalkingPad/KingSmith trovati ({len(walkingpads)}):")
        for i, d in enumerate(walkingpads, 1):
            print(f"  {i}. {d.name} ({d.address})")
    else:
        print("\nNessun dispositivo con nome WalkingPad/KingSmith trovato.")
        print("Cercando dispositivi con servizio 0xFE00...")

        # Seconda passata: cerca per service UUID
        for d in devices:
            if d.metadata and "uuids" in d.metadata:
                uuids = d.metadata["uuids"]
                if any("fe00" in u.lower() for u in uuids):
                    walkingpads.append(d)
                    print(f"  Trovato via UUID: {d.name or 'Senza nome'} ({d.address})")

        if not walkingpads:
            print("  Nessun dispositivo con servizio FE00 trovato.")
            print("\nDispositivi BLE nelle vicinanze (per riferimento):")
            for d in sorted(other_ble, key=lambda x: x.rssi or -999, reverse=True)[:10]:
                rssi = d.rssi or "N/A"
                print(f"  - {d.name} ({d.address}) RSSI={rssi}")

    return walkingpads


# ── Compatibility checks ────────────────────────────────────────

async def run_checks(address: str, name: str = "") -> CompatReport:
    """Esegue tutti i check di compatibilità su un dispositivo.

    SICURO: usa solo comandi di lettura/query. Non muove il nastro.
    """
    report = CompatReport(device_name=name, device_address=address)

    # ── 1. Connessione BLE ──────────────────────────────────
    print(f"\nConnessione a {name or address}...")
    client = BleakClient(address)

    try:
        await client.connect(timeout=15.0)
    except (BleakError, asyncio.TimeoutError, OSError) as e:
        report.add(
            "Connessione BLE",
            CHECK_FAIL,
            f"Impossibile connettersi: {e}",
            critical=True,
        )
        report.print_report()
        return report

    report.add("Connessione BLE", CHECK_PASS, "Connesso con successo")

    try:
        services = client.services

        # ── 2. Servizio FE00 ────────────────────────────────
        svc = services.get_service(SERVICE_UUID)
        if svc:
            report.add(
                "Servizio WalkingPad (0xFE00)",
                CHECK_PASS,
                f"UUID: {svc.uuid}",
                critical=True,
            )
        else:
            # Elenca i servizi trovati per debug
            found_svcs = [s.uuid for s in services]
            report.add(
                "Servizio WalkingPad (0xFE00)",
                CHECK_FAIL,
                f"Non trovato. Servizi presenti:\n" + "\n".join(f"  - {u}" for u in found_svcs),
                critical=True,
            )
            # Senza FE00 è inutile continuare
            report.print_report()
            return report

        # ── 3. Caratteristica Notify (FE01) ─────────────────
        notify_char = services.get_characteristic(NOTIFY_CHAR)
        if notify_char:
            props = notify_char.properties
            has_notify = "notify" in props
            report.add(
                "Caratteristica Notify (0xFE01)",
                CHECK_PASS if has_notify else CHECK_WARN,
                f"Proprietà: {', '.join(props)}"
                + ("" if has_notify else "\nATTENZIONE: 'notify' non presente nelle proprietà"),
                critical=True if not has_notify else False,
            )
        else:
            report.add(
                "Caratteristica Notify (0xFE01)",
                CHECK_FAIL,
                "Non trovata",
                critical=True,
            )

        # ── 4. Caratteristica Write (FE02) ──────────────────
        write_char = services.get_characteristic(WRITE_CHAR)
        if write_char:
            props = write_char.properties
            has_write = "write" in props or "write-without-response" in props
            report.add(
                "Caratteristica Write (0xFE02)",
                CHECK_PASS if has_write else CHECK_WARN,
                f"Proprietà: {', '.join(props)}"
                + ("" if has_write else "\nATTENZIONE: nessuna proprietà write trovata"),
                critical=True if not has_write else False,
            )
        else:
            report.add(
                "Caratteristica Write (0xFE02)",
                CHECK_FAIL,
                "Non trovata",
                critical=True,
            )

        # Se mancano le caratteristiche, non possiamo testare la comunicazione
        if not notify_char or not write_char:
            report.print_report()
            return report

        # ── 5. Sottoscrizione notifiche ─────────────────────
        received_packets = []
        packet_event = asyncio.Event()

        def on_notify(sender, data: bytearray):
            received_packets.append(bytes(data))
            packet_event.set()

        try:
            await client.start_notify(NOTIFY_CHAR, on_notify)
            report.add("Sottoscrizione notifiche", CHECK_PASS)
        except (BleakError, OSError) as e:
            report.add(
                "Sottoscrizione notifiche",
                CHECK_FAIL,
                f"Errore: {e}",
                critical=True,
            )
            report.print_report()
            return report

        # ── 6. Profile handshake ────────────────────────────
        print("  Invio profile handshake...")
        try:
            await client.write_gatt_char(WRITE_CHAR, CMD_PROFILE, response=False)
            await asyncio.sleep(1.5)
            report.add(
                "Profile handshake (CMD_PROFILE)",
                CHECK_PASS,
                "Comando inviato senza errori",
            )
        except (BleakError, OSError) as e:
            report.add(
                "Profile handshake (CMD_PROFILE)",
                CHECK_WARN,
                f"Errore invio: {e}\nPotrebbe non essere necessario per questo modello",
            )

        # ── 7. Status query (CMD_NOOP) ──────────────────────
        print("  Invio status query...")
        packet_event.clear()

        try:
            await client.write_gatt_char(WRITE_CHAR, CMD_NOOP, response=False)
        except (BleakError, OSError) as e:
            report.add(
                "Status query (CMD_NOOP)",
                CHECK_FAIL,
                f"Errore invio: {e}",
                critical=True,
            )
            report.print_report()
            return report

        # Aspetta risposta (max 3 secondi)
        try:
            await asyncio.wait_for(packet_event.wait(), timeout=3.0)
        except asyncio.TimeoutError:
            pass

        if not received_packets:
            report.add(
                "Ricezione risposta",
                CHECK_FAIL,
                "Nessun pacchetto ricevuto entro 3 secondi",
                critical=True,
            )
            report.print_report()
            return report

        report.add(
            "Ricezione risposta",
            CHECK_PASS,
            f"Ricevuti {len(received_packets)} pacchetti",
        )

        # ── 8. Formato pacchetto ────────────────────────────
        # Prova a fare un secondo query per avere un pacchetto "fresco"
        # (il primo potrebbe essere stale)
        packet_event.clear()
        received_packets.clear()
        await client.write_gatt_char(WRITE_CHAR, CMD_NOOP, response=False)

        try:
            await asyncio.wait_for(packet_event.wait(), timeout=3.0)
        except asyncio.TimeoutError:
            pass

        if received_packets:
            pkt = received_packets[-1]
            pkt_hex = pkt.hex()
            pkt_len = len(pkt)

            # Header check
            has_header = pkt[:2] == RESP_HEADER
            # Length check
            good_length = pkt_len >= 17

            details = []
            details.append(f"Lunghezza: {pkt_len} byte (attesi >= 17)")
            details.append(f"Header: {pkt[:2].hex()} (atteso: f8a2)")
            details.append(f"Raw: {pkt_hex}")

            if has_header and good_length:
                report.add(
                    "Formato pacchetto",
                    CHECK_PASS,
                    "\n".join(details),
                )
            elif has_header and not good_length:
                report.add(
                    "Formato pacchetto",
                    CHECK_WARN,
                    "\n".join(details) + "\nPacchetto più corto del previsto, potrebbe essere un modello diverso",
                )
            else:
                report.add(
                    "Formato pacchetto",
                    CHECK_FAIL,
                    "\n".join(details) + "\nHeader non riconosciuto — protocollo diverso",
                    critical=True,
                )

            # ── 9. Parse status ─────────────────────────────
            status = parse_status(pkt)
            if status:
                details_s = []
                details_s.append(f"belt_state: {status.belt_state}")
                details_s.append(f"speed: {status.speed_kmh:.1f} km/h")
                details_s.append(f"mode: {status.manual_mode} ({'auto' if status.manual_mode == 0 else 'manual' if status.manual_mode == 1 else 'standby'})")
                details_s.append(f"time: {status.time_s}s")
                details_s.append(f"distance: {status.dist_m:.0f}m")
                details_s.append(f"steps: {status.steps}")
                details_s.append(f"controller_button: {status.controller_button}")

                report.add(
                    "Parsing stato dispositivo",
                    CHECK_PASS,
                    "\n".join(details_s),
                )

                # ── 10. Valori plausibili ───────────────────
                issues = []
                if status.speed_kmh > 12.0:
                    issues.append(f"Velocità anomala: {status.speed_kmh} km/h (max atteso ~12)")
                if status.belt_state not in (0, 1, 3, 5, 7, 8, 9):
                    issues.append(f"belt_state sconosciuto: {status.belt_state}")
                if status.manual_mode not in (0, 1, 2):
                    issues.append(f"manual_mode sconosciuto: {status.manual_mode}")
                if status.steps > 99999:
                    issues.append(f"Conteggio passi anomalo: {status.steps}")

                if not issues:
                    report.add(
                        "Valori plausibili",
                        CHECK_PASS,
                        "Tutti i campi hanno valori nel range atteso",
                    )
                else:
                    report.add(
                        "Valori plausibili",
                        CHECK_WARN,
                        "\n".join(issues),
                    )
            else:
                report.add(
                    "Parsing stato dispositivo",
                    CHECK_FAIL,
                    "Impossibile parsare il pacchetto come stato WalkingPad",
                    critical=True,
                )

        else:
            report.add(
                "Formato pacchetto",
                CHECK_SKIP,
                "Nessun pacchetto fresco ricevuto per la verifica",
            )

        # ── 11. Query parametri ─────────────────────────────
        print("  Invio query parametri...")
        packet_event.clear()
        received_packets.clear()

        try:
            await client.write_gatt_char(WRITE_CHAR, CMD_QUERY_PARAMS, response=False)
            await asyncio.sleep(1.0)

            if received_packets:
                report.add(
                    "Query parametri (CMD_QUERY_PARAMS)",
                    CHECK_PASS,
                    f"Ricevuti {len(received_packets)} pacchetti in risposta",
                )
            else:
                report.add(
                    "Query parametri (CMD_QUERY_PARAMS)",
                    CHECK_WARN,
                    "Nessuna risposta — alcuni modelli non supportano questa query",
                )
        except (BleakError, OSError) as e:
            report.add(
                "Query parametri (CMD_QUERY_PARAMS)",
                CHECK_WARN,
                f"Errore: {e}",
            )

        # ── 12. Device name check ───────────────────────────
        device_name = name or ""
        if any(kw in device_name.upper() for kw in KNOWN_PREFIXES):
            report.add(
                "Nome dispositivo",
                CHECK_PASS,
                f'"{device_name}" corrisponde ai pattern noti',
            )
        elif device_name:
            report.add(
                "Nome dispositivo",
                CHECK_WARN,
                f'"{device_name}" non corrisponde ai pattern noti '
                f"({', '.join(KNOWN_PREFIXES)})\n"
                "Il driver non lo troverà con la scansione automatica.\n"
                "Soluzione: usare l'indirizzo BLE diretto oppure aggiornare il filtro nel driver.",
            )
        else:
            report.add(
                "Nome dispositivo",
                CHECK_WARN,
                "Nome non disponibile — la scansione automatica potrebbe non trovarlo.\n"
                "Soluzione: usare l'indirizzo BLE diretto.",
            )

        # ── 13. Elenco completo servizi (per debug) ─────────
        all_services = []
        for svc in services:
            chars = []
            for c in svc.characteristics:
                chars.append(f"    {c.uuid} [{', '.join(c.properties)}]")
            all_services.append(f"  {svc.uuid}")
            all_services.extend(chars)

        report.add(
            "Mappa servizi BLE completa",
            CHECK_PASS,
            "\n".join(all_services),
        )

        # ── Cleanup ─────────────────────────────────────────
        try:
            await client.stop_notify(NOTIFY_CHAR)
        except Exception:
            pass

    finally:
        try:
            await client.disconnect()
        except Exception:
            pass

    report.print_report()
    return report


# ── Main ────────────────────────────────────────────────────────

async def main():
    address = None
    name = ""

    if len(sys.argv) > 1:
        address = sys.argv[1]
        print(f"Check diretto su: {address}")
    else:
        devices = await scan_devices()
        if not devices:
            print("\nNessun dispositivo trovato. Assicurati che il treadmill sia acceso")
            print("e nelle vicinanze, poi riprova.")
            print("\nSe conosci l'indirizzo BLE, puoi specificarlo direttamente:")
            print("  python walkingpad_compat_check.py <indirizzo>")
            sys.exit(1)

        if len(devices) == 1:
            address = devices[0].address
            name = devices[0].name or ""
            print(f"\nUn solo dispositivo trovato, procedo con il check...")
        else:
            print("\nSeleziona il dispositivo da testare (numero):")
            while True:
                try:
                    choice = int(input("> ")) - 1
                    if 0 <= choice < len(devices):
                        address = devices[choice].address
                        name = devices[choice].name or ""
                        break
                    print(f"Inserisci un numero tra 1 e {len(devices)}")
                except (ValueError, EOFError):
                    print("Input non valido")

    report = await run_checks(address, name)

    # Exit code per automazione
    sys.exit(0 if report.compatible else 1)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.WARNING,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )
    asyncio.run(main())
