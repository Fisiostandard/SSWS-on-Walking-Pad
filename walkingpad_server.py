"""
WalkingPad Web Server
=====================
Interfaccia web per controllare il WalkingPad e registrare sessioni cliniche.
Usa il driver BLE nativo (walkingpad_driver.py) — nessuna dipendenza da ph4-walkingpad.

Avvia con: python3 walkingpad_server.py
Poi apri nel browser: http://localhost:5050

Opzioni:
  python3 walkingpad_server.py                           # usa indirizzo salvato
  python3 walkingpad_server.py --address XX:XX:XX:XX     # indirizzo manuale
  python3 walkingpad_server.py --scan                    # cerca WalkingPad via BLE
"""

import argparse
import asyncio
import json
import logging
import os
import queue
import signal
import subprocess
import sys
import threading
import time
import uuid
from datetime import datetime
from flask import Flask, Response, jsonify, request, send_from_directory
import requests as http_requests

from walkingpad_driver import WalkingPadDriver
from walkingpad_protocol import WalkingPadStatus

# ── Configurazione ───────────────────────────────────────────
DEFAULT_ADDRESS = os.environ.get("WALKINGPAD_ADDRESS", "")
CONFIG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".walkingpad_address")

# Server clinico remoto
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CLINICAL_SERVER_URL = os.environ.get("CLINICAL_SERVER_URL", "").rstrip("/")
CLINICAL_API_TOKEN = os.environ.get("CLINICAL_API_TOKEN", "")
VAULT_SERVER_URL = os.environ.get("VAULT_SERVER_URL", "").rstrip("/")
VAULT_API_TOKEN = os.environ.get("VAULT_API_TOKEN", "")

# Fallback: leggi token da file se non in env
def _read_config_file(filename, default=""):
    path = os.path.join(BASE_DIR, filename)
    if os.path.exists(path):
        with open(path) as f:
            return f.read().strip()
    return default

if not CLINICAL_SERVER_URL:
    CLINICAL_SERVER_URL = _read_config_file(".clinical_server_url", "https://3d-ga.it")
if not CLINICAL_API_TOKEN:
    CLINICAL_API_TOKEN = _read_config_file(".clinical_api_token")
if not VAULT_SERVER_URL:
    VAULT_SERVER_URL = _read_config_file(".vault_server_url", "https://vault.3d-ga.it")
if not VAULT_API_TOKEN:
    VAULT_API_TOKEN = _read_config_file(".vault_api_token")

app = Flask(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(name)s] %(levelname)s: %(message)s",
    datefmt="%H:%M:%S",
)

# ── Stato condiviso tra thread ───────────────────────────────
state = {
    "running": False,
    "speed_kmh": 0.0,
    "dist_m": 0.0,
    "steps": 0,
    "elapsed_s": 0.0,
    "max_speed_kmh": 0.0,
    "log": [],
    "error": None,
    "status_msg": "Pronto",
}
sse_queue: queue.Queue = queue.Queue()
cmd_queue: queue.Queue = queue.Queue()  # comandi da Flask → thread BLE (es. cambio sensibilità)
pad_thread = None
start_time_ref = None


def _get_address() -> str:
    """Recupera l'indirizzo BLE del WalkingPad dalla configurazione."""
    if DEFAULT_ADDRESS:
        return DEFAULT_ADDRESS
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE) as f:
            addr = f.read().strip()
            if addr:
                return addr
    return ""


def _save_address(address: str):
    """Salva l'indirizzo per le sessioni future."""
    with open(CONFIG_FILE, "w") as f:
        f.write(address)


# ── Callback tamper (telecomando premuto) ────────────────────
def on_tamper(msg: str):
    """Chiamato quando il driver rileva una manomissione dal telecomando."""
    state["tamper"] = True
    state["tamper_msg"] = msg
    state["tamper_time"] = datetime.now().strftime("%H:%M:%S")
    # Invia evento SSE speciale per notificare il browser
    tamper_event = json.dumps({
        "type": "tamper",
        "msg": msg,
        "time": state["tamper_time"],
    })
    sse_queue.put(tamper_event)


# ── Callback status WalkingPad ───────────────────────────────
def on_status(status: WalkingPadStatus):
    global start_time_ref

    # Salva sempre app_speed per la logica di controllo velocità
    state["app_speed_raw"] = status.app_speed

    if not state["running"] or start_time_ref is None:
        return

    elapsed = time.time() - start_time_ref
    speed_kmh = status.speed_kmh
    dist_m = status.dist_m
    steps = status.steps

    state["speed_kmh"] = speed_kmh
    state["dist_m"] = dist_m
    state["steps"] = steps
    state["elapsed_s"] = round(elapsed, 1)
    if speed_kmh > state["max_speed_kmh"]:
        state["max_speed_kmh"] = speed_kmh

    row = {
        "timestamp": datetime.now().strftime("%H:%M:%S"),
        "elapsed_s": round(elapsed, 1),
        "speed_kmh": round(speed_kmh, 1),
        "dist_m": round(dist_m, 1),
        "steps": steps,
    }
    state["log"].append(row)
    sse_queue.put(json.dumps(row))


# ── Loop asyncio WalkingPad (gira in thread separato) ────────
def pad_thread_fn(settings: dict, address: str):
    global start_time_ref

    async def run():
        global start_time_ref

        try:
            driver = WalkingPadDriver(address=address)
            driver.on_status = on_status
            driver.on_tamper = on_tamper

            state["tamper"] = False
            state["tamper_msg"] = ""
            state["status_msg"] = "Connessione al WalkingPad..."

            success = await driver.connect()
            if not success:
                state["error"] = "Impossibile connettersi al WalkingPad"
                state["running"] = False
                return

            await asyncio.sleep(2.0)

            # Configurazione
            max_speed_units = int(settings["max_speed"] * 10)
            await driver.set_max_speed(max_speed_units)
            await asyncio.sleep(0.5)

            # Sensibilità sensore piede (1=alta, 2=media, 3=bassa)
            sens = int(state.get("sensitivity", 2))
            await driver.set_sensitivity(sens)
            await asyncio.sleep(0.5)

            # MODE_AUTO: il sensore piede del WalkingPad controlla la velocità.
            await driver.set_mode(0)  # MODE_AUTO
            await asyncio.sleep(0.5)
            await driver.start_belt()
            await asyncio.sleep(5.0)  # attende fine countdown (9→8→7→1)

            start_time_ref = time.time()
            state["running"] = True
            state["error"] = None
            state["status_msg"] = "Nastro avviato — cammina alla tua velocità."

            # MODE_AUTO: il WalkingPad gestisce la velocità autonomamente.
            # Il software monitora e aggiorna la sensibilità se richiesto.
            while state["running"]:
                await asyncio.sleep(0.5)
                while not cmd_queue.empty():
                    try:
                        cmd = cmd_queue.get_nowait()
                        if cmd["type"] == "sensitivity":
                            await driver.set_sensitivity(cmd["value"])
                            logging.getLogger("walkingpad").info(
                                "Sensibilità cambiata a %d", cmd["value"])
                    except queue.Empty:
                        break

        except Exception as e:
            logging.getLogger("walkingpad").error("Errore thread: %s", e)
            state["error"] = str(e)
            state["running"] = False
        finally:
            try:
                await driver.stop_belt()
                await asyncio.sleep(0.5)
                await driver.disconnect()
            except Exception:
                pass

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(run())
    loop.close()


# ── Routes Flask ─────────────────────────────────────────────
@app.route("/")
def index():
    return send_from_directory(".", "walkingpad_ui.html")


@app.route("/start", methods=["POST"])
def start():
    global pad_thread, start_time_ref

    # Se il thread precedente è morto, resetta lo stato
    if state["running"] and (pad_thread is None or not pad_thread.is_alive()):
        state["running"] = False

    if state["running"]:
        return jsonify({"ok": False, "msg": "Sessione già in corso"})

    address = _get_address()
    if not address:
        return jsonify({"ok": False, "msg": "Indirizzo WalkingPad non configurato. "
                        "Usa --address o --scan all'avvio, oppure imposta "
                        "la variabile WALKINGPAD_ADDRESS."})

    data = request.json
    state["log"] = []
    state["speed_kmh"] = 0.0
    state["dist_m"] = 0.0
    state["steps"] = 0
    state["elapsed_s"] = 0.0
    state["max_speed_kmh"] = 0.0
    state["error"] = None
    state["paziente"] = data.get("paziente", "")
    state["running"] = False
    start_time_ref = None

    state["sensitivity"] = int(data.get("sensitivity", 2))  # 1=alta, 2=media, 3=bassa
    settings = {
        "max_speed": float(data.get("max_speed", 6.0)),
    }

    pad_thread = threading.Thread(
        target=pad_thread_fn,
        args=(settings, address),
        daemon=True,
    )
    pad_thread.start()
    return jsonify({"ok": True})


@app.route("/stop", methods=["POST"])
def stop():
    state["running"] = False
    return jsonify({"ok": True})


@app.route("/set_sensitivity", methods=["POST"])
def set_sensitivity():
    """Cambia sensibilità sensore piede durante la sessione.
    level: 1=alta, 2=media, 3=bassa."""
    data = request.json or {}
    level = int(data.get("level", 2))
    level = max(1, min(3, level))
    state["sensitivity"] = level
    cmd_queue.put({"type": "sensitivity", "value": level})
    return jsonify({"ok": True, "level": level})


@app.route("/mark_ssws", methods=["POST"])
def mark_ssws():
    """Registra una marcatura SSWS dall'esaminatore."""
    data = request.json or {}
    marker = {
        "timestamp": datetime.now().strftime("%H:%M:%S"),
        "elapsed_s": round(state.get("elapsed_s", 0), 1),
        "speed_kmh": round(data.get("speed_kmh", state.get("speed_kmh", 0)), 2),
        "speed_ms": round(data.get("speed_kmh", state.get("speed_kmh", 0)) / 3.6, 3),
        "method": data.get("method", "manual"),  # manual | auto
    }
    state.setdefault("ssws_markers", []).append(marker)
    logging.getLogger("walkingpad").info(
        "SSWS marcata: %.2f km/h (%.3f m/s) a %s",
        marker["speed_kmh"], marker["speed_ms"], marker["timestamp"],
    )
    return jsonify({"ok": True, "marker": marker})


@app.route("/restart", methods=["POST"])
def restart():
    """Riavvia il server: lancia un nuovo processo e uccide questo."""
    state["running"] = False

    def _do_restart():
        time.sleep(0.5)  # lascia il tempo di inviare la risposta HTTP
        # Lancia una nuova istanza con gli stessi argomenti
        subprocess.Popen([sys.executable] + sys.argv)
        time.sleep(0.5)  # lascia partire il nuovo processo
        os.kill(os.getpid(), signal.SIGTERM)

    threading.Thread(target=_do_restart, daemon=True).start()
    return jsonify({"ok": True, "msg": "Riavvio in corso..."})


@app.route("/shutdown", methods=["POST"])
def shutdown():
    """Spegne il server Flask e libera la porta."""
    state["running"] = False

    def _do_shutdown():
        time.sleep(0.5)
        os.kill(os.getpid(), signal.SIGTERM)

    threading.Thread(target=_do_shutdown, daemon=True).start()
    return jsonify({"ok": True})


@app.route("/status")
def status():
    return jsonify(state)


@app.route("/stream")
def stream():
    def event_stream():
        while True:
            try:
                data = sse_queue.get(timeout=2)
                yield f"data: {data}\n\n"
            except queue.Empty:
                yield ": ping\n\n"
    return Response(
        event_stream(),
        mimetype="text/event-stream",
        headers={"Cache-Control": "no-cache, no-store", "X-Accel-Buffering": "no"},
    )


@app.route("/download")
def download():
    if not state["log"]:
        return "Nessun dato", 404
    paziente = state.get("paziente", "sessione").replace(" ", "_")
    filename = f"{paziente}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

    def generate():
        keys = state["log"][0].keys()
        yield ",".join(keys) + "\n"
        for row in state["log"]:
            yield ",".join(str(v) for v in row.values()) + "\n"

    return Response(
        generate(),
        mimetype="text/csv",
        headers={"Content-Disposition": f"attachment; filename={filename}"},
    )


# ── Invio dati al server clinico ──────────────────────────────
@app.route("/send_to_server", methods=["POST"])
def send_to_server():
    """
    Proxy: risolve identità via vault, poi invia dati sessione al server clinico.
    Il browser non vede mai i token API.

    Flusso:
    1. Flask → vault.3d-ga.it/api/lookup-or-create/ (nome+cognome+CF → pseudo_id)
    2. Flask → 3d-ga.it/api/treadmill-session/ (pseudo_id + dati clinici, MAI nomi)
    """
    data = request.json or {}
    log = logging.getLogger("walkingpad.upload")

    # ── Validazione configurazione ──
    if not CLINICAL_API_TOKEN or not VAULT_API_TOKEN:
        return jsonify({"ok": False, "msg": "Token API non configurati. "
                        "Imposta CLINICAL_API_TOKEN e VAULT_API_TOKEN."}), 500

    # ── Validazione input ──
    last_name = data.get("cognome", "").strip()
    first_name = data.get("nome", "").strip()
    fiscal_code = data.get("codice_fiscale", "").strip().upper()

    if not last_name or not first_name:
        return jsonify({"ok": False, "msg": "Nome e cognome obbligatori."}), 400
    if not fiscal_code:
        return jsonify({"ok": False, "msg": "Codice fiscale obbligatorio."}), 400

    # ── Sicurezza: rifiuta invio su HTTP in produzione ──
    # TODO: rimuovere ALLOW_HTTP_UPLOAD dopo attivazione HTTPS su 3d-ga.it
    allow_http = os.environ.get("ALLOW_HTTP_UPLOAD", "") or _read_config_file(".allow_http_upload")
    if not allow_http:
        for url in [VAULT_SERVER_URL, CLINICAL_SERVER_URL]:
            if url and not url.startswith("https://") and "localhost" not in url and "127.0.0.1" not in url:
                log.warning("Rifiuto invio a URL non HTTPS: %s", url)
                return jsonify({"ok": False, "msg": f"Impossibile inviare dati a URL non HTTPS: {url}. "
                                "Per test, crea il file .allow_http_upload con contenuto 'yes'."}), 400

    # ── Step 1: Risolvi identità via vault → pseudo_id ──
    try:
        vault_resp = http_requests.post(
            f"{VAULT_SERVER_URL}/api/lookup-or-create/",
            json={"fiscal_code": fiscal_code, "last_name": last_name, "first_name": first_name},
            headers={"Authorization": f"Bearer {VAULT_API_TOKEN}"},
            timeout=10,
        )
        if vault_resp.status_code not in (200, 201):
            error_detail = vault_resp.json().get("error", vault_resp.text)
            log.error("Vault error %d: %s", vault_resp.status_code, error_detail)
            return jsonify({"ok": False, "msg": f"Errore identity vault: {error_detail}"}), 502

        vault_data = vault_resp.json()
        pseudo_id = vault_data["pseudo_id"]
        log.info("Identity vault: %s → %s (created=%s)",
                 fiscal_code, pseudo_id, vault_data.get("created"))

    except http_requests.exceptions.ConnectionError:
        return jsonify({"ok": False, "msg": "Identity vault non raggiungibile. Controlla la connessione."}), 502
    except http_requests.exceptions.Timeout:
        return jsonify({"ok": False, "msg": "Identity vault timeout."}), 504
    except Exception as e:
        log.exception("Errore vault inatteso")
        return jsonify({"ok": False, "msg": f"Errore vault: {str(e)}"}), 500

    # ── Step 2: Invia dati clinici al server (solo pseudo_id, MAI nomi) ──
    # Determina SSWS dal primo marker o dallo stato
    ssws_markers = state.get("ssws_markers", [])
    ssws_kmh = None
    ssws_ms = None
    ssws_method = "unknown"

    if ssws_markers:
        ssws_kmh = ssws_markers[-1].get("speed_kmh", 0)
        ssws_ms = ssws_markers[-1].get("speed_ms", 0)
        ssws_method = ssws_markers[-1].get("method", "manual")

    # Genera UUID sessione per idempotency
    session_uuid = data.get("session_uuid", str(uuid.uuid4()))

    clinical_payload = {
        "pseudo_id": pseudo_id,
        "session_date": datetime.now().strftime("%Y-%m-%d"),
        "ssws_kmh": ssws_kmh,
        "ssws_ms": ssws_ms,
        "ssws_method": ssws_method,
        "duration_s": state.get("elapsed_s", 0),
        "distance_m": state.get("dist_m", 0),
        "steps": state.get("steps", 0),
        "max_speed_kmh": state.get("max_speed_kmh", 0),
        "tamper_detected": state.get("tamper", False),
        "session_uuid": session_uuid,
        "log": state.get("log", []),
        "ssws_markers": ssws_markers,
        "notes": data.get("notes", ""),
    }

    try:
        clinical_resp = http_requests.post(
            f"{CLINICAL_SERVER_URL}/api/treadmill-session/",
            json=clinical_payload,
            headers={"Authorization": f"Bearer {CLINICAL_API_TOKEN}"},
            timeout=30,
        )

        if clinical_resp.status_code in (200, 201):
            result = clinical_resp.json()
            log.info("Dati inviati: %s, trial #%s, SSWS=%.3f m/s",
                     pseudo_id, result.get("trial_number"), ssws_ms or 0)
            return jsonify({
                "ok": True,
                "pseudo_id": pseudo_id,
                "trial_number": result.get("trial_number"),
                "ssws_ms": result.get("ssws_ms"),
                "msg": "Dati salvati sul server clinico.",
            })
        else:
            error_detail = clinical_resp.json().get("error", clinical_resp.text)
            log.error("Clinical server error %d: %s", clinical_resp.status_code, error_detail)
            return jsonify({"ok": False, "msg": f"Errore server clinico: {error_detail}"}), 502

    except http_requests.exceptions.ConnectionError:
        return jsonify({"ok": False, "msg": "Server clinico non raggiungibile."}), 502
    except http_requests.exceptions.Timeout:
        return jsonify({"ok": False, "msg": "Server clinico timeout."}), 504
    except Exception as e:
        log.exception("Errore clinical server inatteso")
        return jsonify({"ok": False, "msg": f"Errore: {str(e)}"}), 500


@app.route("/server_config")
def server_config():
    """Restituisce lo stato della configurazione server (senza esporre token)."""
    return jsonify({
        "clinical_configured": bool(CLINICAL_API_TOKEN),
        "vault_configured": bool(VAULT_API_TOKEN),
        "clinical_url": CLINICAL_SERVER_URL,
        "vault_url": VAULT_SERVER_URL,
    })


# ── Compatibility check ─────────────────────────────────────────
compat_state = {
    "running": False,
    "done": False,
    "checks": [],
    "compatible": None,
    "device_name": "",
    "device_address": "",
    "error": None,
}


def _compat_thread_fn(address: str):
    """Esegue il compatibility check in un thread separato."""
    from walkingpad_compat_check import run_checks

    async def _run():
        compat_state["running"] = True
        compat_state["done"] = False
        compat_state["checks"] = []
        compat_state["error"] = None
        compat_state["compatible"] = None

        try:
            report = await run_checks(address, compat_state.get("device_name", ""))
            compat_state["checks"] = [
                {
                    "name": c.name,
                    "status": c.status,
                    "detail": c.detail,
                    "critical": c.critical,
                }
                for c in report.checks
            ]
            compat_state["compatible"] = report.compatible
            compat_state["device_name"] = report.device_name
            compat_state["device_address"] = report.device_address
        except Exception as e:
            compat_state["error"] = str(e)
            compat_state["compatible"] = False
        finally:
            compat_state["running"] = False
            compat_state["done"] = True

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(_run())
    loop.close()


@app.route("/compat_check", methods=["POST"])
def compat_check():
    """Avvia un compatibility check sul WalkingPad configurato."""
    if compat_state["running"]:
        return jsonify({"ok": False, "msg": "Check già in corso"})

    if state["running"]:
        return jsonify({"ok": False, "msg": "Sessione in corso — ferma prima la sessione"})

    address = _get_address()
    if not address:
        return jsonify({"ok": False, "msg": "Nessun indirizzo WalkingPad configurato"})

    compat_state["device_address"] = address
    t = threading.Thread(target=_compat_thread_fn, args=(address,), daemon=True)
    t.start()
    return jsonify({"ok": True, "msg": "Check avviato"})


@app.route("/compat_check_status")
def compat_check_status():
    """Restituisce lo stato corrente del compatibility check."""
    return jsonify(compat_state)


# ── Main ─────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="WalkingPad Web Interface")
    parser.add_argument("--address", type=str, default="",
                        help="Indirizzo BLE del WalkingPad")
    parser.add_argument("--scan", action="store_true",
                        help="Scansiona per trovare WalkingPad nelle vicinanze")
    parser.add_argument("--port", type=int, default=5050,
                        help="Porta del server web (default: 5050)")
    args = parser.parse_args()

    # Scansione BLE
    if args.scan:
        print("\nScansione BLE in corso...")
        devices = asyncio.run(WalkingPadDriver.scan(timeout=5.0))
        if devices:
            print(f"\nTrovati {len(devices)} WalkingPad:")
            for i, (addr, name) in enumerate(devices):
                print(f"  [{i+1}] {name} ({addr})")
            if len(devices) == 1:
                addr = devices[0][0]
                _save_address(addr)
                print(f"\nIndirizzo salvato: {addr}")
            else:
                try:
                    choice = int(input("\nScegli dispositivo (numero): ")) - 1
                    addr = devices[choice][0]
                    _save_address(addr)
                    print(f"Indirizzo salvato: {addr}")
                except (ValueError, IndexError):
                    print("Scelta non valida")
                    return
        else:
            print("Nessun WalkingPad trovato. Assicurati che sia acceso.")
            return

    # Indirizzo da argomento
    if args.address:
        _save_address(args.address)

    address = _get_address()

    print(f"\n{'='*50}")
    print("  WalkingPad Web Interface")
    print("  Driver BLE nativo (senza ph4-walkingpad)")
    if address:
        print(f"  Dispositivo: {address}")
    else:
        print("  ATTENZIONE: nessun indirizzo configurato!")
        print("  Usa: --scan oppure --address <INDIRIZZO>")
    print(f"  Apri nel browser: http://localhost:{args.port}")
    print(f"{'='*50}\n")

    app.run(host="0.0.0.0", port=args.port, threaded=True)


if __name__ == "__main__":
    main()
