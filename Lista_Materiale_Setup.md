# Lista del Materiale Necessario per il Setup Sperimentale

Questo documento elenca l'hardware e il software necessari per allestire l'esperimento di validazione del tapis roulant Kingsmith WalkingPad contro il 10-Meter Walk Test (10MWT). Le opzioni proposte sono orientate a un buon compromesso tra affidabilità scientifica e costo contenuto (approccio *low-cost*), reperibili sul mercato (es. Amazon Italia o rivenditori di elettronica).

---

## 1. Materiale per il 10-Meter Walk Test (Gold Standard)

Per cronometrare i 10 metri centrali del test (su 14 metri totali di pista) eliminando l'errore dei riflessi umani, hai due opzioni principali:

### Opzione A: Sistema a Fotocellule (Cronometraggio Hardware Preciso)
Ideale se vuoi un sistema "chiavi in mano" affidabilissimo per le pubblicazioni.

*   **Sistema di Cronometraggio Wireless Sportivo (es. *Cenipar* o similari su Amazon):**
    *   *Cos'è:* Un kit composto da un display LED/LCD e due coppie di fotocellule wireless (partenza e arrivo) montate su treppiedi.
    *   *Come funziona:* Posizioni una fotocellula al metro 2 e l'altra al metro 12. Quando il paziente taglia il primo raggio il tempo parte, al secondo si ferma.
    *   *Prezzo indicativo:* 150€ - 300€ su Amazon.it (Cerca "Cronometro sportivo fotocellule wireless" o "Sprint timer").
    *   *Alternativa Pro:* Sistemi professionali usati in atletica (es. Witty Microgate), ma i costi salgono sopra i 1000€.

### Opzione B: Analisi Video (Cronometraggio Software)
Ideale se vuoi spendere meno e avere anche la documentazione video del cammino.

*   **Smartphone con buon framerate (60fps o 120fps):** (Probabilmente già in tuo possesso).
*   **Treppiede per Smartphone:** Essenziale per mantenere l'inquadratura perfettamente ferma. (Costo: 20-30€ su Amazon).
*   **Software di Video Analisi (Gratuito):**
    *   *Kinovea (PC Windows):* Gratuito, open source, standard de facto per la videoanalisi sportiva/riabilitativa. Permette di inserire un cronometro a schermo e misurare il tempo esatto al millisecondo in cui il bacino del paziente supera il marker dei 2m e dei 12m.
    *   *Dartfish Express / Hudl Technique (iOS/Android):* App per smartphone che permettono lo scorrimento frame by frame.

*   **Nastro adesivo colorato (es. nastro carta giallo o rosso):** Per segnare a terra le linee 0m, 2m, 12m, 14m.

---

## 2. Materiale per "Hackerare" il Kingsmith WalkingPad (Setup Self-Paced)

L'obiettivo è far sì che il tapis roulant adatti la velocità in base alla posizione del paziente sul tappeto in modo fluido, superando i limiti del software di fabbrica.

### Il "Cervello" del Sistema

*   **Raspberry Pi 4 Model B (o Raspberry Pi 5):**
    *   *Cos'è:* Un mini-computer completo grande come una carta di credito. Ha il Bluetooth integrato (per parlare con il tapis roulant) e porte GPIO/USB per collegare i sensori.
    *   *Cosa comprare:* Kit completo (Scheda + Alimentatore + Case + Scheda MicroSD). Evita le versioni con poca RAM, meglio 4GB o 8GB.
    *   *Prezzo indicativo:* 80€ - 120€ su Amazon.it o rivenditori ufficiali (es. Melopero, Kubii).
    *   *Link esempio (Amazon Italia):* [Raspberry Pi 5 8 GB Starter Kit (db-tronic)](https://www.amazon.it/Raspberry-Alimentatore-Ufficiale-Alloggiamento-Dissipatore/dp/B0CRPF47RG/ref=sr_1_6?crid=1SD7OND7PBWT&dib=eyJ2IjoiMSJ9.ptP7J3FZcmbYoZvFxUp_VoHgopWyH2_bwsvE7F9TbDxgtZLJsdilLkxReACu1nLc2Ne13t8Jfb-E7sIdpGyw9gUJh8hlwI9W4t43P6n78hMmcSlwdbtJVrVvBPmyj9iYCsxHw-hTgDN-sY1_bMeOSp4WcVB14FirUIzqw_-Uw7p41aNuhJY0o3_yChiB_cUapczBx3iONyd6xQRNb_ZenRu5hrfyAck-JW3vrCTl1i7Ewgf75yUXV2WMLABszAWNJLonitCc8ObzPIQB2l69hJLKexJUqlx8CIOLOHVJWIU.riQa16EmwizPLznDYhvsXjfg9M9sS30rFT6KLs57uZg&dib_tag=se&keywords=raspberry%2Bpi%2B5&qid=1773072001&sprefix=raspberr%2Caps%2C308&sr=8-6&ufe=app_do%3Aamzn1.fos.fca66a76-6518-40f2-959f-2dca30e9c5d1&th=1)
    *   *Nota:* al momento il link puo risultare non disponibile; verificare sempre in fase ordine che sia la variante corretta (Raspberry Pi 5, 4GB o 8GB, alimentatore ufficiale 27W).
    *   *Alternativa:* Un qualsiasi PC portatile (Windows/Mac/Linux) con Bluetooth, se non vuoi usare il Raspberry. Il PC portatile è più ingombrante ma ti evita di comprare il Raspberry se ne hai già uno vecchio da dedicare.

### Interfaccia Operatore (Consigliata: Tablet)

Per uso ambulatoriale, il controllo del sistema avviene tramite web app locale, senza dover usare un computer durante i test.

*   **Tablet (scelta consigliata):**
    *   *Cosa comprare:* iPad base (10"/11") oppure tablet Android equivalente.
    *   *Uso:* apre la pagina web del Raspberry (`http://raspberrypi.local:5000`) per Start, Pausa, Stop, Ricalibra e monitoraggio.
    *   *Prezzo indicativo:* 200€ - 450€ (in base al modello).
*   **Smartphone (alternativa):**
    *   *Uso:* stessa web app del tablet, utile come backup.
*   **Supporto tablet da parete o da banco:**
    *   *Motivo:* rende il setup piu elegante e stabile in ambulatorio.
    *   *Prezzo indicativo:* 20€ - 60€.

### Sistema Video (Frontale + Laterale)

*   **2 webcam UVC 1080p (30 fps):**
    *   una camera frontale e una laterale per ripresa simultanea del cammino.
    *   *Scelta consigliata:* **Logitech C922 Pro** (2 pezzi uguali).
    *   *Prezzo indicativo:* 60€ - 80€ per webcam.
*   **Hub USB 3.0 alimentato (consigliato):**
    *   migliora la stabilita quando usi due webcam con Raspberry.
    *   *Posizionamento:* vicino a una presa elettrica (cosi alimenti hub + periferiche in modo stabile).
    *   *Nota alimentazione:* normalmente **non** va usato per alimentare il Raspberry Pi. Il Raspberry deve avere il suo alimentatore dedicato ufficiale USB-C 27W.
*   **SSD USB esterno (consigliato 1TB):**
    *   archivio locale dei video con spazio sufficiente per molte sessioni.
*   **Supporti fissi per webcam (parete):**
    *   inquadrature ripetibili e coerenti tra sessioni.
    *   *Specifica tecnica:* staffa con **vite 1/4"-20** (standard fotografico) e testa a sfera.
    *   *Scelta consigliata:* staffa a parete tipo NEEWER/RAYWOW con vite 1/4" (2 pezzi).
    *   *Prezzo indicativo:* 15€ - 25€ per staffa.

### Il "Sensore" (L'Occhio del Sistema)

Per capire dove si trova il paziente sul tappeto (troppo avanti = deve accelerare; troppo indietro = deve rallentare), useremo un sensore LiDAR che misuri la distanza in continuo.

*   **Sensore LiDAR a singolo punto (Scelta definitiva)**
    *   *Cos'è:* Un sensore laser che misura la distanza decine di volte al secondo. E una soluzione precisa, stabile e adatta a un setup clinico ripetibile.
    *   *Cosa comprare:* **TF-Luna LiDAR** (Benewake) o **TFmini-S**.
    *   *Collegamento:* via USB (con adattatore UART-USB) oppure direttamente ai pin del Raspberry Pi.
    *   *Prezzo indicativo:* 30€ - 40€ su Amazon.it o negozi di robotica (Mouser, RS Components).
    *   *Adattatore USB (se usato con PC):* Modulo convertitore USB a TTL CH340 o FT232 (Costo: 5€ - 10€).
    *   *Posizionamento consigliato:* montaggio fisso dietro il paziente (a muro o supporto stabile), ad altezza bacino, con calibrazione software a inizio test.

### Supporti e Cavi

*   **Supporto di montaggio stabile (preferibile fissaggio a muro):** Per montare il sensore LiDAR ad altezza bacino, puntato verso il paziente. In alternativa, treppiede/asta telescopica. (Costo: 20-30€ per supporto base).
*   **Cavo prolunga USB (2-3 metri):** Se colleghi il sensore al PC o al Raspberry Pi.
*   **Canaline/fascette per cablaggio:** Per fissare i cavi e ridurre rischi di inciampo.

### Software di Controllo (Web App su Raspberry)

*   **Sistema operativo Raspberry Pi OS (Bookworm):** base del sistema.
*   **Python 3 + librerie:** `flask` (o `fastapi`), `pyserial` (LiDAR), libreria Bluetooth per WalkingPad.
*   **Servizio automatico all'avvio (systemd):** avvia il controller senza intervento manuale.
*   **Browser su tablet/smartphone:** Safari/Chrome per interfaccia operatore.
*   **(Opzionale) Accesso remoto tecnico:** SSH per manutenzione e aggiornamenti.

---

## Sintesi del Carrello Ideale (Budget stimato: ~450€ - 900€ con tablet)

1.  Sensore TF-Luna LiDAR (~35€)
2.  Adattatore USB-TTL per il sensore (~8€)
3.  Raspberry Pi 4 Kit Completo (Opzionale, puoi usare un PC) (~100€)
4.  2 webcam Logitech C922 (~120€ - 160€ totali)
5.  2 staffe a parete con vite 1/4" (~30€ - 50€ totali)
6.  Hub USB 3.0 alimentato (~25€ - 45€)
7.  SSD USB esterno 1TB (~60€ - 100€)
8.  Supporto fisso LiDAR (parete/treppiede) (~20€ - 30€)
9.  Tablet (consigliato) o smartphone dedicato (~200€ - 450€ per tablet)
10. Supporto tablet da banco/parete (~20€ - 60€)
11. Nastro carta colorato (~5€)
12. Sistema Fotocellule per 10MWT (Opzionale, puoi usare smartphone+Kinovea per iniziare) (~150€)

*Nota: Prima di acquistare il sensore e il Raspberry Pi, assicurati che il modello esatto del tuo Kingsmith WalkingPad sia compatibile con le librerie Bluetooth open-source esistenti (come `ph4-walkingpad`), testando la connessione dal tuo computer.*