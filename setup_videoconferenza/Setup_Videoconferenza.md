# Setup Videoconferenza in Ambulatorio (con Raspberry Pi)

Questo documento raccoglie tutte le indicazioni operative emerse per usare il Raspberry anche per videochiamate in ambulatorio, mantenendo stabilita e ordine nel setup clinico.

---

## 1) Risposta breve

Si, **Raspberry Pi 5** puo gestire videochiamate (Zoom/Meet/Jitsi), ma conviene organizzare il sistema a **modalita separate**:

- Modalita Test Clinico: LiDAR + controllo tapis roulant + registrazione video test
- Modalita Videoconferenza: chiamata con colleghi a distanza

Regola: **mai tutte le funzioni insieme**.

---

## 2) Un solo Raspberry basta?

Si, **uno solo puo bastare** se:

- non fai test clinico e videocall contemporaneamente;
- passi da una modalita all'altra chiudendo i servizi non necessari;
- usi Raspberry Pi 5 (meglio 8GB per maggiore margine).

---

## 3) Perche non fare tutto insieme

Se sullo stesso dispositivo fai contemporaneamente:

- controllo real-time del tapis roulant,
- acquisizione LiDAR,
- doppia registrazione webcam,
- videochiamata live,

aumenti il rischio di:

- latenza e jitter,
- frame persi,
- instabilita generale,
- competizione tra applicazioni per le stesse webcam.

Per uno studio clinico serve priorita all'affidabilita del test.

---

## 4) Webcam e condivisione tra software

In pratica una webcam USB viene gestita bene da una sola applicazione alla volta.
Quindi:

- in modalita test: webcam usate dal software di registrazione;
- in modalita call: webcam usate dalla piattaforma di videoconferenza.

Meglio evitare sovrapposizioni.

---

## 5) Cablaggio: come tenerlo pulito e sicuro

La soluzione piu robusta resta cablata USB per le webcam.

Note pratiche:

- ogni webcam USB di solito prende alimentazione dallo stesso cavo USB (non serve alimentatore separato per ciascuna);
- usare hub USB 3.0 alimentato migliora la stabilita;
- passare i cavi in canaline adesive a parete;
- evitare cavi a terra nelle zone di passaggio paziente.

---

## 6) Architettura consigliata in ambulatorio

- Raspberry Pi 5 fisso (preferibilmente montato in posizione protetta)
- 2 webcam cablate (frontale + laterale) per i test
- tablet/iPad come pannello di controllo web locale
- eventuale webcam dedicata alla videocall (opzionale ma utile)
- SSD esterno per salvataggio video e log

---

## 7) Workflow operativo a modalita

### Modalita A - Test Clinico

1. Avvio servizio test
2. Calibrazione LiDAR
3. Registrazione video frontale/laterale
4. Esecuzione prova
5. Salvataggio file sessione
6. Stop servizio test

### Modalita B - Videoconferenza

1. Stop servizi test
2. Avvio browser/app call
3. Selezione webcam e audio
4. Chiamata
5. Fine call
6. Ripristino servizi test (se necessario)

---

## 8) Dove salvare i video

Scelta consigliata:

- salvataggio locale su SSD USB esterno collegato al Raspberry;
- struttura cartelle per data/soggetto/sessione;
- backup periodico su NAS o disco esterno secondario.

Questo evita saturazione microSD e migliora affidabilita.

---

## 9) Decisione pratica finale

Per il tuo contesto:

- **Si, un solo Raspberry e sufficiente**.
- Va usato a **profili separati** (test o call).
- Per stabilita e valore scientifico, il test clinico ha sempre priorita rispetto alla videocall.
