# Caratteristiche Software Python (Bozza Requisiti)

Questo documento definisce i criteri tecnici minimi del software Python per controllare il Kingsmith in modalita self-paced con sensore LiDAR.

L'obiettivo e ottenere una regolazione della velocita fluida, ripetibile e sicura per pazienti ortopedici.

---

## 1) Principi di progetto

- Controllo robusto a piccoli cambi di setup fisico (treppiede non sempre identico).
- Comandi di velocita graduali, mai bruschi.
- Sicurezza prima della performance (fail-safe sempre attivo).
- Tracciabilita completa: ogni test deve produrre log esportabili.

---

## 2) Input e acquisizione dati

- Sensore primario: LiDAR (es. TF-Luna o TFmini-S).
- Frequenza di acquisizione target: 20-50 Hz.
- Timestamp monotono per ogni campione.
- Validazione campioni: scartare valori fuori range fisico plausibile.

---

## 3) Calibrazione obbligatoria a inizio sessione

La posizione del treppiede puo variare di qualche mm/cm tra una sessione e l'altra.
Per questo il software non deve usare soglie assolute fisse.

Requisiti:

- Step guidato di calibrazione (5-10 s) con paziente fermo in posizione neutra.
- Calcolo baseline `d0` come media/mediana di N campioni validi.
- Definizione errore relativo: `e(t) = d_filtrata(t) - d0`.
- Salvataggio di `d0` nel report di sessione.

Nota: in questo modo il sistema resta stabile anche se il sensore e posizionato leggermente piu avanti o indietro.

---

## 4) Filtri e stabilizzazione segnale

- Filtro anti-rumore obbligatorio:
  - mediana su finestra breve, oppure
  - media mobile esponenziale.
- Deadband (zona morta) attorno a `e=0` per evitare micro-correzioni continue.
  - Valore iniziale consigliato: +/- 2 cm.
- Anti-jitter: non inviare comandi se la variazione resta dentro deadband.

---

## 5) Logica di controllo velocita

Schema consigliato:

- Se `e < -deadband`: paziente avanti -> accelerare.
- Se `e > +deadband`: paziente indietro -> rallentare.
- Se `|e| <= deadband`: mantenere velocita.

Vincoli obbligatori:

- Passo massimo comando: 0.1 km/h per aggiornamento.
- Limite di variazione temporale (ramp rate): es. max 0.2-0.3 km/h al secondo.
- Intervallo minimo tra comandi: es. 200-500 ms.
- Clamp su velocita minima/massima impostata dal protocollo clinico.

---

## 6) Sicurezza (fail-safe)

Il software deve prevedere sempre:

- Pulsante STOP software + tasto/emergency stop fisico del tapis roulant.
- Timeout sensore: se il LiDAR non manda dati validi per > X ms -> rallentamento progressivo e stop.
- Timeout comunicazione Bluetooth: stessa logica di stop sicuro.
- Check di coerenza: se misure impossibili (salto troppo grande) -> ignora campione e segnala warning.

---

## 7) Interfaccia operatore

Minimo indispensabile:

- Schermata con distanza live, errore relativo, velocita corrente.
- Stato connessioni (LiDAR e Bluetooth).
- Bottoni: Start test, Pause, Stop, Recalibra.
- Prompt guidati per operatore (calibrazione completata, warning, fine prova).

---

## 8) Logging e output dati

Per ogni sessione salvare:

- ID soggetto, data/ora, operatore.
- Parametri usati: deadband, filtro, ramp rate, limiti velocita.
- Baseline `d0`.
- Serie temporale (timestamp, distanza raw, distanza filtrata, errore, velocita comandata, velocita letta).
- Eventi: start, pause, stop, warning, fail-safe.

Formato consigliato:

- CSV per analisi statistica (Excel, R, Python).
- JSON/YAML per metadati di configurazione.

---

## 9) Workflow test consigliato

1. Connessione sensore e tapis roulant.
2. Calibrazione baseline (5-10 s).
3. Fase familiarizzazione paziente (3-5 min, dati opzionali).
4. Prova valida (2-3 min) con registrazione completa.
5. Esportazione automatica file dati.

---

## 10) Criteri di accettazione software (v1)

Il software e pronto per studio pilota se:

- Non produce accelerazioni percepite come brusche in soggetti test.
- Recupera automaticamente piccole variazioni di posizionamento del sensore tramite calibrazione.
- Gestisce perdita sensore/Bluetooth in modo sicuro (rallenta e stop).
- Produce log completi e leggibili per analisi ICC/Bland-Altman.
- Parametri configurabili senza modificare codice (file config).

---

## 11) Parametri iniziali suggeriti (da tarare sul campo)

- Frequenza loop controllo: 10 Hz.
- Deadband: 2 cm.
- Filtro: media mobile esponenziale alpha=0.25.
- Step velocita: 0.1 km/h.
- Ramp rate massimo: 0.25 km/h/s.
- Timeout sensore: 500 ms.
- Timeout Bluetooth: 1000 ms.

Questi valori sono un punto di partenza, non definitivi.
La taratura finale va fatta su soggetti reali con supervisione clinica.
