# Checklist Videocall Ambulatorio (Raspberry)

Checklist rapida per usare il Raspberry in modalita videoconferenza in modo ordinato e sicuro.

---

## 1) Prima della chiamata (Pre-call)

- [ ] Verificare che **non** sia in corso un test clinico su tapis roulant.
- [ ] Fermare eventuali servizi test (LiDAR/registrazione test).
- [ ] Controllare alimentazione Raspberry e stabilita rete Wi-Fi.
- [ ] Verificare webcam selezionata per la call (frontale dedicata o principale).
- [ ] Verificare microfono e audio in uscita.
- [ ] Aprire piattaforma (Zoom/Meet/Jitsi) e fare test audio/video.
- [ ] Verificare sfondo/inquadratura professionale (senza dati paziente visibili).

---

## 2) Durante la chiamata

- [ ] Tenere chiuse applicazioni non necessarie.
- [ ] Monitorare qualità rete (latenza/audio/video).
- [ ] Non avviare registrazioni test clinici in parallelo.
- [ ] Non cambiare webcam da software esterni durante la call.
- [ ] Se la qualità degrada: ridurre risoluzione video call (es. 720p).

---

## 3) Fine chiamata (Post-call)

- [ ] Chiudere piattaforma videoconferenza.
- [ ] Verificare che webcam e audio siano stati rilasciati.
- [ ] Riattivare servizi test solo se serve.
- [ ] Annotare eventuali problemi tecnici riscontrati.

---

## 4) Passaggio a Modalita Test Clinico

- [ ] Avviare servizi test (web app + controller LiDAR + registrazione).
- [ ] Eseguire calibrazione LiDAR pre-test (5-10 s).
- [ ] Verificare doppia camera test (frontale + laterale).
- [ ] Verificare cartella di salvataggio e spazio disponibile.
- [ ] Eseguire prova breve di 10 secondi prima del paziente.

---

## 5) Regole di sicurezza e privacy

- [ ] Nessun nome/cognome paziente nei file video (usare codici soggetto).
- [ ] Cavi fissati in canaline, nessun cavo in area di passaggio.
- [ ] Pulsante STOP tapis roulant sempre accessibile.
- [ ] Backup periodico dei dati su supporto esterno sicuro.

---

## 6) Troubleshooting rapido

### Webcam non rilevata

- [ ] Scollegare/ricollegare webcam.
- [ ] Provare altra porta USB 3.0.
- [ ] Riavviare hub USB alimentato.

### Audio scarso

- [ ] Controllare microfono corretto nelle impostazioni call.
- [ ] Ridurre rumore ambientale.
- [ ] Usare cuffia/mic esterno se necessario.

### Call instabile

- [ ] Verificare segnale Wi-Fi.
- [ ] Chiudere processi pesanti.
- [ ] Ridurre qualita video.
