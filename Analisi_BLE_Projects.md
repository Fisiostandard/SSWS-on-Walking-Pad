# Analisi progetti BLE WalkingPad - 2026-03-19

Analisi comparativa di tre progetti per il controllo del tapis roulant KingSmith WalkingPad via BLE, finalizzata a estrarre tecniche utili per il nostro driver minimale.

---

## 1. DorianRudolph/QWalkingPad (C++/Qt)

**Repo:** https://github.com/DorianRudolph/QWalkingPad
**Linguaggio:** C++ con Qt6
**Protocollo:** Reverse-engineered indipendentemente (non usa ph4-walkingpad)

### Protocollo BLE

**Service UUID:** `0xfe00`
**Caratteristiche:**
- `0xfe01` - Read/Notify (ricezione dati dal dispositivo)
- `0xfe02` - Write (invio comandi al dispositivo)

Identiche a ph4-walkingpad. Nessuna divergenza sugli UUID.

### Formato messaggi

**Byte message (6 byte):** `0xf7, 0xa2, [key], [value], [checksum], 0xfd`
- Checksum = `0xa2 + key + value`

**Integer message (9 byte):** `0xf7, 0xa6, [key], 0x00, [byte3], [byte2], [byte1], [checksum], 0xfd`
- Valore a 24 bit (big-endian) distribuito su 3 byte
- Checksum = somma dei byte da posizione 1 a 6

**Sync record (6 byte):** `0xf7, 0xa7, 0xaa, [n], [checksum], 0xfd`

**NOTA:** ph4-walkingpad usa `0xf8` come header delle risposte (248 decimale), QWalkingPad parsa risposte con header `0xa2`, `0xa6`, `0xa7` al byte[1]. I comandi usano `0xf7` (247) come header in entrambi.

### Strutture dati parsate

**Info (risposta 0xa2, >=15 byte):**
- state (uint8), speed (uint8), mode (uint8)
- time (uint32, 24-bit), distance (uint32, 24-bit), steps (uint32, 24-bit)

**Params (risposta 0xa6, >=14 byte):**
- goalType, regulate, maxSpeed, startSpeed, startMode, sensitivity, display, lock, unit
- goal (uint32)

**Record (risposta 0xa7, >=18 byte):**
- onTime, startTime, duration, distance, steps (tutti uint32)
- remainingRecords (uint8)

### Costanti protocollo

| Costante | Valore |
|---|---|
| MODE_AUTO | 0 |
| MODE_MANUAL | 1 |
| MODE_SLEEP | 2 |
| SENSITIVITY_HIGH | 1 |
| SENSITIVITY_MEDIUM | 2 |
| SENSITIVITY_LOW | 3 |
| UNIT_METRIC | 0 |
| UNIT_IMPERIAL | 1 |

Display flags (bitfield): TIME=0b1, SPEED=0b10, DISTANCE=0b100, CALORIE=0b1000, STEP=0b10000

### Timing e stabilita connessione

**Elemento critico - command throttling a 50ms:**
```
sendTimer->setInterval(50);  // "the WalkingPad ignores commands if they come in too quickly"
```
Il WalkingPad IGNORA i comandi che arrivano troppo velocemente. QWalkingPad usa una coda di comandi e ne invia uno ogni 50ms.

**Polling interval:** 1000ms (1 secondo) per query stato, parametri e record.

**Confronto con ph4-walkingpad:** ph4 usa 690ms di intervallo minimo tra comandi - molto piu conservativo. QWalkingPad a 50ms e piu aggressivo ma funziona.

### Riconnessione automatica

- Salva l'indirizzo dell'ultimo dispositivo connesso
- Al riavvio, tenta connessione automatica se `autoReconnect` e abilitato
- Timeout di 5 secondi per il recupero record prima di abortire

### Tecniche utili da adottare

1. **Coda comandi con throttling** - Approccio pulito: accoda tutto, invia a intervallo fisso
2. **Timeout espliciti** - 5s per recupero record
3. **Riconnessione automatica basata su indirizzo salvato**
4. **Parsing con validazione lunghezza** - Verifica `>=15`, `>=14`, `>=18` byte prima di parsare

---

## 2. CodeJawn/walkingpad (Python/Flask)

**Repo:** https://github.com/CodeJawn/walkingpad
**Linguaggio:** Python + HTML
**BLE:** Usa `ph4-walkingpad` come dipendenza (non reimplementa il protocollo)
**Web framework:** Flask + Waitress

### Architettura

Questo progetto e il piu simile al nostro approccio (web + BLE). Usa:
- Thread BLE dedicato con asyncio event loop proprio
- Flask per servire l'interfaccia web
- Polling attivo: `await controller.ask_stats()` ogni secondo nel loop `_stats_monitor()`

### Pattern interessanti

**1. Auto-pause con grace period:**
```python
_auto_pause_grace_until = time.time() + 7  # 7 secondi di grazia dopo resume
```
Quando il tappeto si ferma inaspettatamente (velocita a 0 mentre dovrebbe correre), il sistema:
- Salva la velocita corrente dalla speed_history (deque di 15 letture)
- Setta `belt_running = False`
- Al resume, applica un grace period di 7 secondi per evitare che transitori di velocita riattivino l'auto-pause

**2. Speed history buffer:**
```python
speed_history = deque(maxlen=15)  # Ultimi 15 campioni di velocita
```
Usato per determinare a quale velocita riprendere dopo una pausa. Prende il valore piu vecchio del buffer (la velocita stabile prima del calo).

**3. Gestione dual-access (dict e attributi):**
La callback di stato gestisce sia dict che oggetti con attributi per leggere distance/steps/speed - difesa contro cambiamenti nell'API di ph4-walkingpad.

**4. Cumulative stats con delta tracking:**
Non si fida dei valori assoluti dal dispositivo. Calcola delta tra letture successive e li accumula. Gestisce il wrap-around (quando i valori del dispositivo calano, resetta il baseline).

**5. Sequenza resume robusta:**
```
STANDBY -> MANUAL -> start belt -> set speed -> restart monitor
```
Con flag `belt_running = True` settato ottimisticamente prima della sequenza.

**6. Cache-Control headers:**
```python
response.headers["Cache-Control"] = "no-store"
```
Su endpoint `/stats` per evitare che il browser cachi dati vecchi.

### Costanti

| Costante | Valore |
|---|---|
| MAX_SPEED_KMH | 6.0 |
| MIN_SPEED_KMH | 1.0 |
| SPEED_STEP | 0.6 km/h |
| SLOW_WALK_SPEED_KMH | 4.5 |
| KCAL_PER_MILE | 95 |

### Limitazioni osservate

- Usa `os._exit(0)` per lo shutdown (non pulito)
- Thread BLE come daemon: se muore, non c'e recovery automatico
- Nessun meccanismo di heartbeat o watchdog sulla connessione BLE
- Error handling generico (`except Exception`) in molti punti

---

## 3. ph4-walkingpad - Analisi issue aperti

### Problemi critici da evitare nel nostro driver

**A. Pacchetti malformati / lunghezza variabile (Issue #16)**
- Il parser crasha con `bytearray index out of range` su pacchetti incompleti o malformati
- Pacchetto problematico: `[f8, a2, 00, 00, 01, 00, 00, 00, 00, 00, 00]` (11 byte invece dei 15+ attesi)
- Workaround: flag `--ignore-bad-packets` prolunga il funzionamento ma alla fine i dati si fermano
- **LEZIONE: Il nostro parser DEVE validare la lunghezza prima di accedere ai byte per indice**

**B. Asyncio event loop conflicts (Issue #16, #10, #19)**
- `Task got Future attached to a different loop` - errore ricorrente
- Su Windows, creazione esplicita di `ProactorEventLoop` conflitta con loop esistente
- Python 3.10+ cambia il comportamento di asyncio, rompendo il codice
- **LEZIONE: Usare un singolo event loop, non crearne di nuovi. Testare su Python 3.10+**

**C. Caratteristiche BLE mancanti su alcuni modelli (Issue #23)**
- Il WalkingPad Z1 NON espone `0xfe01` e `0xfe02`
- Le variabili `char_fe01` e `char_fe02` rimangono None, causando crash
- **LEZIONE: Verificare SEMPRE che le caratteristiche esistano prima di usarle**

**D. Discovery automatico fallisce (Issue #12)**
- La scansione trova il dispositivo ma il codice non propaga l'indirizzo
- Workaround: specificare l'indirizzo MAC manualmente
- **LEZIONE: Supportare sia discovery che indirizzo manuale, con fallback**

**E. Comandi che non hanno effetto (Issue #10)**
- Il dispositivo si connette e bippa, ma start/speed non muovono il tappeto
- I valori di stato cambiano ma il motore non risponde
- Potrebbe essere un problema di sequenza di inizializzazione mancante
- **LEZIONE: Verificare la sequenza completa: connect -> mode MANUAL -> start -> speed**

**F. ATT Error 0x80 (Issue #22)**
- Errore D-Bus durante richiesta statistiche
- Codice ATT non documentato nello standard BLE
- **LEZIONE: Gestire errori ATT non standard con retry o skip**

**G. Comandi che ritornano None (Issue #13)**
- `status`, `start`, `stop` ritornano `None` anche su dispositivo attivo
- Errore in dbus_fast su write_callback con buffer None
- **LEZIONE: Verificare il risultato di ogni write BLE**

### Riepilogo issue per categoria

| Categoria | Issue | Severita |
|---|---|---|
| Pacchetti malformati | #16 | CRITICA |
| Event loop asyncio | #10, #16, #19 | ALTA |
| Modelli incompatibili | #23, #17 | MEDIA |
| Discovery fallisce | #12 | MEDIA |
| Comandi senza effetto | #10, #13 | ALTA |
| ATT errors | #22 | MEDIA |
| Windows compatibility | #19 | MEDIA |

---

## Raccomandazioni per il nostro driver minimale

### 1. Formato protocollo (confermato da 2 implementazioni indipendenti)

```
Comandi:   0xf7 [type] [key] [value] [checksum] 0xfd
Risposte:  0xf8 [type] [data...] [checksum] 0xfd
Checksum:  sum(bytes[1:-2]) % 256
```

Service `0xfe00`, Char Read `0xfe01`, Char Write `0xfe02`.

### 2. Timing

| Parametro | QWalkingPad | ph4-walkingpad | CodeJawn | Raccomandazione |
|---|---|---|---|---|
| Min inter-command | 50ms | 690ms | (usa ph4) | **100-200ms** (conservativo ma reattivo) |
| Polling interval | 1000ms | variabile | 1000ms | **1000ms** |
| Reconnect timeout | - | - | - | **5000ms** |
| Command timeout | - | - | - | **3000ms** |

### 3. Checklist robustezza (basata su bug reali)

- [ ] Validare lunghezza pacchetto PRIMA di parsare (Issue #16)
- [ ] Verificare esistenza caratteristiche BLE dopo discovery (Issue #23)
- [ ] Supportare indirizzo MAC manuale come fallback (Issue #12)
- [ ] Gestire errori ATT non standard con retry (Issue #22)
- [ ] Non creare event loop espliciti - usare `asyncio.get_event_loop()` (Issue #19)
- [ ] Coda comandi con throttling per evitare che il WalkingPad ignori comandi
- [ ] Delta tracking per statistiche cumulative (pattern CodeJawn)
- [ ] Grace period dopo resume per evitare falsi auto-pause (pattern CodeJawn)
- [ ] Speed history buffer per recovery velocita dopo pausa (pattern CodeJawn)
- [ ] Cache-Control: no-store sugli endpoint dati (pattern CodeJawn)

### 4. Comandi essenziali per il nostro caso d'uso (SSWS measurement)

Per la misurazione della SSWS ci servono solo:
1. `query()` - polling stato (velocita, distanza, passi, tempo)
2. `setSpeed(v)` - impostare velocita
3. `setMode(MANUAL)` - modo manuale
4. `start()` - avviare il tappeto

Non ci servono: record sync, calibrazione, settings display, auto mode.

### 5. Differenze tra i progetti

| Aspetto | ph4-walkingpad | QWalkingPad | CodeJawn |
|---|---|---|---|
| Implementazione protocollo | Propria | Propria (indipendente) | Usa ph4 |
| Header comandi | 0xf7 | 0xf7 | (ph4) |
| Header risposte | 0xf8 | Parsa da byte[1] | (ph4) |
| Checksum | sum(cmd[1:-2]) % 256 | sum specifico per tipo | (ph4) |
| Speed divisore | /10 | /10 (implicito) | /10 |
| Distance divisore | /100 | parseInt 24-bit | /100 |
| Inter-command delay | 690ms fisso | 50ms (coda) | (ph4) |
| Robustezza pacchetti | Fragile (crashano) | Validazione lunghezza | Try/except generico |

I due reverse-engineering indipendenti concordano sulla struttura del protocollo. Le differenze sono solo implementative, non protocollari.
