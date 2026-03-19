# Setup Video Pulito (Frontale + Laterale)

Questo documento definisce un setup pratico per registrare in simultanea il cammino da due angolazioni:

- camera frontale (fronte paziente)
- camera laterale (profilo)

con integrazione al test SSWS su Kingsmith.

---

## 1) Obiettivo operativo

Durante ogni prova devono partire insieme:

- controllo self-paced (LiDAR + Raspberry + tapis roulant)
- registrazione video frontale
- registrazione video laterale

con salvataggio ordinato per soggetto/sessione.

---

## 2) Il Raspberry puo controllare 2 webcam?

Si, **Raspberry Pi 5** puo farlo, ma con alcune condizioni:

- webcam UVC standard (plug and play su Linux)
- preferibilmente webcam con output MJPEG/H.264 (meno carico CPU)
- uso di porte USB 3.0
- meglio usare un hub USB alimentato se una webcam non viene vista in modo stabile

Per questo progetto il Pi 5 4GB o 8GB e sufficiente.

---

## 3) Hardware consigliato

### Camere

- 2 webcam 1080p (30 fps), UVC, con autofocus disattivabile
- una frontale, una laterale
- supporti fissi (parete o treppiede robusto)

### Connettivita e alimentazione

- Raspberry Pi 5 (gia previsto)
- alimentatore ufficiale 27W
- hub USB 3.0 alimentato (consigliato per stabilita)

### Archiviazione

- SSD USB esterno (almeno 500GB, consigliato 1TB)
- filesystem exFAT o ext4

---

## 4) Software di registrazione

Due opzioni valide.

### Opzione A (consigliata): `ffmpeg` headless

Vantaggi:

- affidabile e leggero
- perfetto per avvio automatico da web app
- salva file gia pronti per analisi

Approccio:

- apri due stream (`/dev/video0` e `/dev/video1`)
- salvi due file separati per ogni sessione
- nomi file coerenti (es. `S001_front_...mp4`, `S001_side_...mp4`)

### Opzione B: OBS Studio

Vantaggi:

- interfaccia grafica semplice

Svantaggi:

- piu pesante su Raspberry
- meno adatto ad avvio completamente automatico

Per uso clinico ripetibile, meglio Opzione A.

---

## 5) Sincronizzazione con il test

La web app del Raspberry deve gestire un flusso unico:

1. Start Sessione
2. Calibrazione LiDAR (5-10 s)
3. Start registrazione video (entrambe le camere)
4. Start test tapis roulant
5. Stop test
6. Stop registrazione video
7. Salvataggio e report

In aggiunta:

- inserire evento di sincronizzazione (beep o flash) all'inizio registrazione
- scrivere timestamp comune nei log sensore e nei metadati video

---

## 6) Cartelle e naming (fondamentale)

Struttura consigliata:

- `data/video/YYYY-MM-DD/SUBJ_XXX/`
- `data/logs/YYYY-MM-DD/SUBJ_XXX/`

File tipici:

- `SUBJ_XXX_front_trial01.mp4`
- `SUBJ_XXX_side_trial01.mp4`
- `SUBJ_XXX_lidar_trial01.csv`
- `SUBJ_XXX_events_trial01.json`

---

## 7) Quanto spazio serve per i video

Indicativo per 2 camere 1080p:

- 4-8 Mbps per camera (dipende dal codec/compressione)
- totale 8-16 Mbps
- circa 1.2-2.4 GB per 20 minuti totali di registrazione

Conclusione: SSD da 1TB e ampiamente sufficiente per molte sessioni.

---

## 8) Best practice cliniche

- inquadrare marcatori a terra e corpo intero
- evitare controluce e riflessi
- bloccare esposizione/focus automatici quando possibile
- verificare 10 secondi di test video prima di ogni sessione
- anonimizzare i file (codice soggetto, no nome/cognome)

---

## 9) Decisione pratica raccomandata

Per partire in modo pulito:

- Raspberry Pi 5 + 2 webcam UVC 1080p + hub USB alimentato
- registrazione con `ffmpeg`
- salvataggio su SSD USB esterno
- controllo unificato da tablet via web app

Questa configurazione e sufficientemente semplice da gestire in ambulatorio e robusta per uno studio pilota.
