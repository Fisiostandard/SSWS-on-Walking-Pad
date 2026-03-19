# Protocollo di Validazione: Kingsmith WalkingPad vs 10-Meter Walk Test (10MWT)

Questo documento delinea i passi operativi, i requisiti tecnici e i riferimenti bibliografici per condurre uno studio di validazione del tapis roulant Kingsmith modificato per la misurazione della *Self-Selected Walking Speed* (SSWS). L'obiettivo è validare lo strumento contro il *Gold Standard* clinico attuale: il 10MWT.

---

## 1. Requisiti dello Studio (Soggetti ed Esaminatori)

*   **Quanti soggetti mi occorrono?**
    Per uno studio di validazione rigoroso servono tra i **35 e i 50 soggetti**. 
    *Fase di validazione tecnica:* Puoi usare soggetti sani (di diverse età per avere un range di velocità vario: dai lenti ai veloci). Non serve che siano già pazienti operati, in questa fase validiamo lo *strumento*. I pazienti li userai nello studio clinico successivo.
*   **Quanti esaminatori?**
    Almeno **2 esaminatori**. 
    Questo serve a dimostrare la *Inter-rater reliability* (affidabilità tra operatori), ovvero che se il Medico A o il Medico B conducono il test sul tapis roulant, il risultato che esce dalla macchina è lo stesso.

---

## 2. Setup del 10-Meter Walk Test (Gold Standard)

*   **Quanto spazio in lunghezza davvero mi occorre minimo?**
    Ti servono **14 metri totali**, rettilinei e senza ostacoli. 
    Il protocollo standard prevede: 2 metri di accelerazione, 10 metri centrali cronometrati, 2 metri di decelerazione. In questo modo misuri la velocità a "regime" per quei 10 metri, senza contare la partenza da fermo e la frenata. Segnerai a terra con del nastro adesivo le linee di inizio (0m), inizio cronometro (2m), fine cronometro (12m), e fine camminata (14m).
*   **Che cosa occorre per il setup? Software vs Cronometri?**
    *   **Opzione Base (Accettata ma prona a errore umano):** Due operatori con cronometri manuali (o smartphone). Lo scarto di riflesso umano su 10 metri (circa 6-10 secondi di test) è statisticamente rilevante.
    *   **Opzione Media (Consigliata):** App per smartphone basate su video. L'operatore riprende il paziente che cammina di lato. Ci sono app di analisi del movimento (es. *Kinovea* su PC o app mobili come *Hudl Technique*) che permettono di calcolare il tempo esatto frame per frame dal passaggio sulla linea dei 2m a quella dei 12m.
    *   **Opzione Avanzata (Fotocellule - Perfetta):** Sistemi di cronometraggio a fotocellule (come quelli da atletica leggera, es. *Microgate* o sistemi cinesi low-cost su Amazon). Annullano totalmente l'errore umano. Il tempo parte quando il paziente taglia il primo raggio laser e si ferma quando taglia il secondo. È inattaccabile.

---

## 3. Setup del Tapis Roulant Kingsmith

Per far sì che il tapis roulant sia *self-paced* (cioè che adatti la sua velocità a quella del paziente), hai bisogno di "hackerare" il modo in cui riceve i comandi.

*   **L'approccio "Pure Software Hack" (Via Bluetooth API):** 
    Il tapis roulant di base ha un telecomando o un'app. Esistono librerie open-source (es. in Python, come `ph4-walkingpad` o `node-noble-xiaomi-kingsmith`) che possono connettersi via Bluetooth al tapis roulant da un computer e inviare comandi di velocità. 
    *   *Il problema:* Come fa il computer a sapere se il paziente sta accelerando o rallentando per mandare il comando giusto? Il Kingsmith A1/R1 ha una modalità "Automatica" basata sulla pressione dei piedi (se cammini verso la testa del tappeto accelera, verso la coda frena). Spesso però questa modalità di fabbrica è brusca e poco fluida.
*   **L'approccio "Raspberry Pi + Sensore LiDAR + Web App":** 
    Questo è il setup ingegneristico ideale. 
    1. Monti un sensore **LiDAR** (es. TF-Luna/TFmini-S), preferibilmente dietro al paziente, in posizione fissa.
    2. Un **Raspberry Pi** legge in continuo la distanza del paziente e comunica via Bluetooth con il Kingsmith.
    3. Lo script di controllo applica la logica self-paced: se il paziente avanza accelera in modo graduale, se arretra rallenta.
    4. L'operatore usa una **web app locale** (da tablet o smartphone) per Start/Pausa/Stop/Ricalibra e monitoraggio.
    *   *Vantaggio:* Hai controllo assoluto sull'algoritmo di accelerazione/decelerazione, interfaccia elegante da ambulatorio, e uso quotidiano senza computer attivo vicino al paziente.

### 3.1 Requisiti software minimi per la Web App

*   **Backend Python sul Raspberry:** `Flask` (o `FastAPI`) per esporre i comandi.
*   **UI Web locale:** pagina HTML responsive per tablet/smartphone.
*   **Comandi minimi:** Start test, Pausa, Stop, Ricalibra.
*   **Indicatori minimi:** stato LiDAR, stato Bluetooth, velocita corrente, timer test.
*   **Avvio automatico:** servizio `systemd` all'accensione del Raspberry.
*   **Salvataggio dati:** CSV per ogni sessione (timestamp, distanza, velocita, eventi).

---

## 4. Svolgimento del Test: Protocollo Operativo

*   **Contestualità:** I test (10MWT e Tapis Roulant) vanno eseguiti **contestualmente (nello stesso giorno)**, uno di seguito all'altro, per ogni soggetto.
*   **Randomizzazione (Fondamentale):** L'ordine non è indifferente a causa dell'effetto affaticamento e dell'effetto apprendimento. Devi **randomizzare** l'ordine:
    *   Il Soggetto 1 fa prima il 10MWT e poi il Tapis Roulant.
    *   Il Soggetto 2 fa prima il Tapis Roulant e poi il 10MWT.
*   **Ripetizioni:** 
    *   *10MWT:* 3 prove. Si fa la media dei tempi o si tiene il migliore.
    *   *Tapis Roulant:* 1 prova di acclimatamento (3-5 minuti, in cui il paziente capisce come funziona il nastro adattivo), seguita da una pausa, e poi 1 prova di misurazione effettiva (2-3 minuti a regime, in cui il computer registra la velocità media di crociera).
*   **Gestione via tablet/smartphone:** Durante il test l'operatore usa la web app del Raspberry come pannello unico di controllo. Il computer non e necessario in sala durante la prova.
*   **Calibrazione pre-test obbligatoria:** Prima di ogni prova su tapis roulant, eseguire 5-10 secondi di calibrazione LiDAR per definire la baseline della sessione.
*   **Video simultanei (frontale + laterale):** Durante la prova valida su tapis roulant avviare entrambe le registrazioni in contemporanea, con timestamp comune della sessione.
*   **Salvataggio dati della sessione:** Ogni prova deve produrre almeno 4 file: video frontale, video laterale, log LiDAR/velocita (CSV), eventi della sessione (JSON).

---

## 5. Letteratura: Il 10MWT in Pazienti con Protesi (THA/TKA)

Se il tuo amico (o un revisore) ti chiede conferma sull'uso del 10MWT come gold standard per queste popolazioni, ecco i riferimenti fondamentali:

1.  **Indoor and outdoor 10-Meter Walk Test and Timed Up and Go in patients after total hip arthroplasty: a reliability and comparative study** *(Archives of Physiotherapy, 2021)*.
    *   *Cosa dice:* Il 10MWT è estremamente affidabile (ICC > 0.90) per misurare la SSWS in pazienti post-THA. Curiosamente, questo studio nota che i pazienti camminano a SSWS diverse se sono al chiuso o all'aperto, confermando la sensibilità della misura all'ambiente (problema che il tuo tapis roulant elimina standardizzando l'ambiente).
2.  **Validity and reliability of performance tests as balance measures in patients with total knee arthroplasty** *(Knee Surgery & Related Research, 2022)*.
    *   *Cosa dice:* Conferma la validità e l'eccellente affidabilità test-retest del 10MWT in pazienti sottoposti a protesi totale di ginocchio (TKA).
3.  **Improvement of walking speed and gait symmetry in older patients after hip arthroplasty: a prospective cohort study** *(BMC Musculoskeletal Disorders, 2016)*.
    *   *Cosa dice:* Dimostra come la velocità di cammino misurata (SSWS) migliori progressivamente nei mesi successivi alla THA e sia un indicatore chiave del successo funzionale dell'operazione.