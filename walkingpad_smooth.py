"""
WalkingPad — Modalità automatica con accelerazione dolce + logging velocità
============================================================================
Versione CLI che usa il driver BLE nativo (nessuna dipendenza da ph4-walkingpad).

USO:
  python3 walkingpad_smooth.py --scan                    # prima volta: trova il device
  python3 walkingpad_smooth.py                           # usa indirizzo salvato
  python3 walkingpad_smooth.py --sensitivity 2           # sensibilità media
  python3 walkingpad_smooth.py --max 3.0 --start 0.3     # max 3 km/h, partenza 0.3
  python3 walkingpad_smooth.py --log sessione1.csv       # salva log personalizzato

Premi Ctrl+C per fermare.
"""

import asyncio
import argparse
import csv
import logging
import os
import time
from datetime import datetime

from walkingpad_driver import WalkingPadDriver
from walkingpad_protocol import WalkingPadStatus, MODE_AUTO

# ── DEFAULT ────────────────────────────────────────────────────
SENSITIVITY  = 3      # 1=alta (reattivo), 2=media, 3=bassa (dolce)
START_SPEED  = 0.5    # km/h
MAX_SPEED    = 6.0    # km/h
CONFIG_FILE  = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".walkingpad_address")
# ──────────────────────────────────────────────────────────────

log_rows = []
start_time = None

logging.basicConfig(
    level=logging.WARNING,
    format="%(asctime)s [%(name)s] %(levelname)s: %(message)s",
    datefmt="%H:%M:%S",
)


def _get_address() -> str:
    addr = os.environ.get("WALKINGPAD_ADDRESS", "")
    if addr:
        return addr
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE) as f:
            return f.read().strip()
    return ""


def _save_address(address: str):
    with open(CONFIG_FILE, "w") as f:
        f.write(address)


def on_status(status: WalkingPadStatus):
    global log_rows, start_time
    if start_time is None:
        return

    elapsed = time.time() - start_time
    speed_kmh = status.speed_kmh
    dist_m = status.dist_m
    steps = status.steps

    log_rows.append({
        "timestamp": datetime.now().strftime("%H:%M:%S.%f")[:-3],
        "elapsed_s": round(elapsed, 1),
        "speed_kmh": speed_kmh,
        "dist_m": dist_m,
        "steps": steps,
    })

    # Barra velocità visiva
    bar_len = int(speed_kmh / 0.2)
    bar = "\u2588" * bar_len + "\u2591" * max(0, 20 - bar_len)

    print(f"  {elapsed:6.1f}s | {bar} {speed_kmh:.1f} km/h | "
          f"dist: {dist_m:.0f}m | passi: {steps}    ", end="\r")


async def main():
    global start_time

    parser = argparse.ArgumentParser(description="WalkingPad accelerazione dolce")
    parser.add_argument("--sensitivity", type=int, default=SENSITIVITY,
                        help="Sensibilità sensore: 1=alta, 2=media, 3=bassa (default: 3)")
    parser.add_argument("--max", type=float, default=MAX_SPEED,
                        help="Velocità massima in km/h (default: 6.0)")
    parser.add_argument("--start", type=float, default=START_SPEED,
                        help="Velocità di partenza in km/h (default: 0.5)")
    parser.add_argument("--log", type=str, default=None,
                        help="Nome file CSV per il log (default: auto con timestamp)")
    parser.add_argument("--address", type=str, default="",
                        help="Indirizzo BLE del WalkingPad")
    parser.add_argument("--scan", action="store_true",
                        help="Scansiona per trovare WalkingPad")
    args = parser.parse_args()

    # Scansione BLE
    if args.scan:
        print("\nScansione BLE in corso...")
        devices = await WalkingPadDriver.scan(timeout=5.0)
        if devices:
            for i, (addr, name) in enumerate(devices):
                print(f"  [{i+1}] {name} ({addr})")
            if len(devices) == 1:
                addr = devices[0][0]
            else:
                try:
                    choice = int(input("Scegli dispositivo: ")) - 1
                    addr = devices[choice][0]
                except (ValueError, IndexError):
                    print("Scelta non valida")
                    return
            _save_address(addr)
            print(f"Indirizzo salvato: {addr}\n")
        else:
            print("Nessun WalkingPad trovato.")
            return

    if args.address:
        _save_address(args.address)

    address = _get_address()
    if not address:
        print("Nessun indirizzo configurato. Usa --scan o --address.")
        return

    log_file = args.log or f"sessione_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

    print(f"\n{'='*60}")
    print(f"  WalkingPad — driver BLE nativo")
    print(f"{'='*60}")
    print(f"  Dispositivo : {address}")
    print(f"  Sensibilità : {args.sensitivity} (1=alta, 3=bassa/dolce)")
    print(f"  Velocità    : {args.start} → max {args.max} km/h")
    print(f"  Log CSV     : {log_file}")
    print(f"{'='*60}\n")

    driver = WalkingPadDriver(address=address)
    driver.on_status = on_status

    print("Connessione in corso...")
    success = await driver.connect()
    if not success:
        print("Impossibile connettersi al WalkingPad.")
        return
    print("Connesso.\n")

    await asyncio.sleep(1.0)
    await driver.set_sensitivity(args.sensitivity)
    await asyncio.sleep(0.3)
    await driver.set_start_speed(int(args.start * 10))
    await asyncio.sleep(0.3)
    await driver.set_max_speed(int(args.max * 10))
    await asyncio.sleep(0.3)
    await driver.set_mode(MODE_AUTO)
    await asyncio.sleep(0.5)

    start_time = time.time()
    print("Nastro pronto. Sali e cammina. Ctrl+C per fermare.\n")

    try:
        while True:
            await asyncio.sleep(1.0)

    except KeyboardInterrupt:
        print("\n\nFermo il nastro...")
        await driver.stop_belt()
        await asyncio.sleep(0.5)
        await driver.disconnect()

        # Salva CSV
        if log_rows:
            with open(log_file, "w", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=log_rows[0].keys())
                writer.writeheader()
                writer.writerows(log_rows)
            elapsed_tot = log_rows[-1]["elapsed_s"]
            max_speed = max(r["speed_kmh"] for r in log_rows)
            avg_speed = sum(r["speed_kmh"] for r in log_rows) / len(log_rows)
            print(f"\n{'='*60}")
            print(f"  Sessione salvata: {log_file}")
            print(f"  Durata    : {elapsed_tot:.0f}s")
            print(f"  Vel. max  : {max_speed:.1f} km/h")
            print(f"  Vel. media: {avg_speed:.1f} km/h")
            print(f"{'='*60}\n")
        else:
            print("Nessun dato registrato.")


if __name__ == "__main__":
    asyncio.run(main())
