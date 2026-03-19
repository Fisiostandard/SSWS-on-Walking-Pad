# Problemi Potenziali — Progetto SSWS Misura

---

## 1. Allucinazione bibliografica nella ricerca letteratura
**Descrizione:** Claude Code ha generato riferimenti bibliografici inventati o con metadati errati (autori, DOI, riviste, titoli fabbricati). Su 18 riferimenti totali nei due file di letteratura, solo 2 erano completamente corretti, 10 avevano errori significativi nei metadati, e 6 erano inventati di sana pianta.

**Gravità:** ALTA — Se usati in una pubblicazione scientifica o in un progetto di ricerca, riferimenti inventati comprometterebbero la credibilità dell'intero lavoro e potrebbero configurare una violazione dell'integrità scientifica.

> #fix 2026-03-12: Verifica sistematica di tutti i riferimenti tramite PubMed/Google Scholar. Rimossi tutti gli articoli inventati, corretti i metadati errati. Aggiunto protocollo anti-allucinazione nel CLAUDE.md che richiede verifica a posteriori con grado di sicurezza 0-1 per ogni informazione. I file Letteratura_SSWS_TapisRoulant.md e Articoli_10MWT_SSWS_Ortopedia.md sono stati riscritti con soli articoli verificati.

---

## 2. Copertura bibliografica insufficiente dopo la pulizia
**Descrizione:** Dopo la rimozione degli articoli errati, restano solo 6 articoli verificati (di cui 2 duplicati tra i file). Diverse aree tematiche fondamentali sono rimaste scoperte: reliability del 10MWT in ortopedia, MCID per SSWS, confronto 10MWT vs 6MWT, validità del treadmill per anziani, wearable sensors.

**Gravità:** MEDIA — Il progetto necessita di una base bibliografica più solida per supportare le scelte metodologiche.

> Mitigazione proposta: eseguire una nuova ricerca bibliografica con verifica immediata di ogni risultato (doppio passaggio come da protocollo CLAUDE.md).

---

## 3. Rischio di citazioni non verificate in futuro
**Descrizione:** Ogni volta che si chiede a un LLM di fornire riferimenti bibliografici, c'è il rischio sistematico di allucinazione. Questo è un problema noto e non eliminabile con i modelli attuali.

**Gravità:** ALTA — Rischio ricorrente ad ogni nuova ricerca.

> #fix 2026-03-12: Protocollo anti-allucinazione inserito in CLAUDE.md. Ogni riferimento bibliografico deve essere verificato con ricerca online e accompagnato da grado di sicurezza. Informazione dubbia sotto 0.95 deve essere segnalata esplicitamente.

---

## 4. Effetto apprendimento nei trial ripetuti del 10MWT
**Descrizione:** Il paziente potrebbe modificare la propria velocità nei trial successivi per "compiacere" l'esaminatore o per ansia da prestazione.

> Mitigazione: trial di familiarizzazione obbligatorio prima della raccolta dati. Istruzione standardizzata e neutra.

---

## 5. Influenza dell'esaminatore sulla velocità del paziente
**Descrizione:** Se l'esaminatore cammina affianco o davanti al paziente, può involontariamente dettare il passo.

> Mitigazione: l'esaminatore deve camminare mezzo passo DIETRO al paziente.

---

## 6. Decelerazione prematura del paziente
**Descrizione:** Il paziente potrebbe rallentare prima della fine della zona cronometrata se vede i segni sul pavimento o le fotocellule.

> Mitigazione: il paziente NON deve sapere dove sono le fotocellule/i punti di cronometraggio. Istruire il paziente a "continuare a camminare fino a quando le dico di fermarsi".

---

## 7. Errore di cronometraggio manuale
**Descrizione:** Con cronometro manuale, l'errore di reazione dell'esaminatore (0.2-0.3s) può influenzare significativamente la misura su distanze brevi.

> Mitigazione: usare fotocellule/timing gates per la ricerca (ICC 0.99-1.00 vs 0.96-0.98 del cronometro).

---

## 8. Setting non standardizzato
**Descrizione:** Corridoi troppo corti, con ostacoli, traffico di persone, o rumorosi possono alterare la misura.

> Mitigazione: corridoio dedicato di almeno 14m, libero, ben illuminato, silenzioso, pavimento uniforme.

---

## 9. Validità del tapis roulant come misura SSWS
**Descrizione:** La letteratura documenta differenze fisiologiche, percettive e biomeccaniche significative tra cammino su tapis roulant e overground. Il tapis roulant NON è validato come outcome measure per SSWS.

> #fix 2026-03-14: decisione di adottare il 10MWT come misura primaria della SSWS.

---

## 10. Aspetti legali ed etici
**Descrizione:** Il protocollo deve essere approvato dal Comitato Etico se coinvolge pazienti. Necessario consenso informato. Rischio caduta per pazienti fragili.

> Mitigazione: supervisione diretta, possibilità di interruzione immediata, documentazione ausili, approvazione CE.

---

## 11. Calzature e ausili non documentati tra sessioni
**Descrizione:** Se il paziente cambia scarpe o ausilio tra le sessioni, la misura non è confrontabile.

> Mitigazione: documentare SEMPRE tipo di calzatura e ausilio ad ogni sessione.

---

## 12. Fatica, dolore e farmaci del paziente
**Descrizione:** Dolore, fatica, farmaci possono influenzare la SSWS in modo significativo.

> Mitigazione: documentare ora del test, livello di dolore (VAS), farmaci assunti, tempo dall'ultimo pasto.

---

## 13. Fotocellule — falso trigger da oscillazione arti
**Descrizione:** Se le fotocellule sono posizionate troppo basse (es. altezza caviglia/ginocchio), l'oscillazione del braccio o della gamba potrebbe interrompere il fascio prima che il tronco raggiunga il gate, generando un falso trigger e un tempo errato.

> Mitigazione: posizionare le fotocellule a 75 cm da terra (livello anca/bacino). Se disponibile, usare configurazione dual beam (doppia fotocellula sovrapposta) che richiede interruzione simultanea di entrambi i fasci.

---

## 14. Fotocellule — paziente consapevole dei punti di cronometraggio
**Descrizione:** Se il paziente nota le fotocellule o i segni a terra, potrebbe decelerare prima del Gate 2 o accelerare dopo il Gate 1, falsando la misura della SSWS.

> Mitigazione: nessun segno a terra. Posizioni dei treppiedi segnate con riferimenti permanenti discreti (punto sul muro/battiscopa). Non menzionare le fotocellule al paziente. Istruire: "cammini fino a quando le dico di fermarsi" (il punto di stop è oltre il Gate 2, a 14m).

---

## 15. Fotocellule — malfunzionamento o mancata registrazione
**Descrizione:** Batterie scariche, disallineamento del fascio, interferenze (luce solare diretta) possono causare mancata registrazione di un trial.

> Mitigazione: test di funzionamento prima di ogni sessione (passare la mano nel fascio). Usare ambiente indoor con illuminazione artificiale. Avere batterie di ricambio. Avere un cronometro manuale come backup.

---

## 16. Controllo BLE del WalkingPad — perdita di connessione durante l'uso
**Descrizione:** Se la connessione BLE si interrompe durante il funzionamento, il tapis roulant continua all'ultima velocità impostata. Non esiste un meccanismo di "dead man's switch" via BLE. I comandi sono inviati come write-without-response (nessun ACK dal dispositivo).

**Gravità:** ALTA — rischio sicurezza per il paziente se il tapis roulant non si ferma.

> Mitigazione proposta: (1) Avere SEMPRE il telecomando fisico a portata di mano come backup per stop immediato. (2) Implementare un heartbeat software che invii periodicamente comandi di status e fermi il tapis roulant se non riceve risposta. (3) Operatore sempre presente accanto al paziente.

---

## 17. Controllo BLE del WalkingPad — cambio velocità senza rampa
**Descrizione:** Il comando BLE imposta direttamente la velocità target. Un salto da 0.5 a 6.0 km/h potrebbe essere eseguito senza rampa graduale (dipende dal firmware del tapis roulant), creando un rischio di caduta.

**Gravità:** ALTA — rischio caduta per il paziente.

> Mitigazione proposta: implementare rampe di velocità software (incrementi di 0.1 km/h ogni 300ms). Mai inviare salti di velocità superiori a 0.5 km/h in un singolo comando.

---

## 18. Controllo BLE del WalkingPad — stabilità della connessione su macOS
**Descrizione:** Multipli report su GitHub di errori ATT (0x80), notification failures, e disconnessioni. macOS 12+ ha un comportamento BLE diverso che richiede scanning prima della connessione e permessi espliciti per Terminal/iTerm2.

**Gravità:** MEDIA — potrebbe richiedere tentativi multipli di connessione e logica di riconnessione robusta.

> Mitigazione proposta: usare Bleak >= 0.14.1, testare approfonditamente la connessione prima dell'uso clinico, implementare logica di riconnessione automatica.

---

## 19. Controllo BLE del WalkingPad — compatibilità modelli
**Descrizione:** Il protocollo è stato reverse-engineered sul modello A1. Il modello R1 Pro ha report di problemi (AttributeError). Non esiste una matrice ufficiale di compatibilità. Il protocollo potrebbe variare tra modelli o revisioni firmware.

**Gravità:** MEDIA — il modello specifico in uso deve essere verificato prima dell'uso clinico.

> Mitigazione proposta: verificare il modello esatto del WalkingPad in uso e testare tutti i comandi prima dell'uso con pazienti.

---

## 20. Controllo BLE del WalkingPad — aspetto medico-legale del controllo programmatico
**Descrizione:** Un dispositivo medico (o usato in contesto clinico) controllato via software non certificato solleva questioni medico-legali. Il software ph4-walkingpad non è un dispositivo medico certificato. In caso di incidente, la responsabilità potrebbe ricadere su chi ha implementato il controllo programmatico.

**Gravità:** ALTA — rischio legale significativo.

> Mitigazione proposta: (1) Documentare chiaramente che il controllo BLE è usato solo per comodità operativa e non sostituisce la supervisione umana. (2) Mantenere sempre il controllo fisico (telecomando) disponibile. (3) Consenso informato del paziente che menziona l'uso di controllo computerizzato. (4) Valutare con il Comitato Etico.

---

## 21. Fotocellule — altezza fascio vs ausili deambulazione
**Descrizione:** Se il paziente usa deambulatore, stampelle o carrozzina, i treppiedi bassi (~25cm) potrebbero non intercettare il passaggio, oppure l'ausilio stesso potrebbe triggerare prima del tronco del paziente.

**Gravità:** MEDIA — misure errate per pazienti con ausili.

> Mitigazione proposta: regolare altezza fascio a ~75cm (livello bacino). Se i treppiedi del kit sono troppo bassi, sostituire con treppiedi fotografici regolabili.

---

## 22. Fotocellule — validazione scientifica del sistema scelto
**Descrizione:** I sistemi economici (Cronox, timer generici cinesi) non hanno pubblicazioni peer-reviewed di validazione. Solo il Microgate Witty ha letteratura scientifica. Per uno studio pubblicabile, i reviewer potrebbero obiettare sullo strumento di misura non validato.

**Gravità:** MEDIA-ALTA per studi pubblicabili, BASSA per uso clinico routinario.

> Mitigazione proposta: (1) Per uso clinico: Cronox è sufficiente (precisione 0.001s). (2) Per pubblicazione: considerare Microgate Witty o citare studi che dimostrano che la precisione 0.001s è clinicamente equivalente per il 10MWT. (3) In alternativa, eseguire uno studio di reliability test-retest del Cronox vs cronometro manuale come studio pilota.

---

## 24. Setup outdoor — interferenze ambientali sulle fotocellule
**Descrizione:** L'uso all'aperto espone le fotocellule IR a interferenze da luce solare diretta (falsi trigger o mancate letture), vento (spostamento treppiedi), e condizioni meteo avverse.

**Gravità:** MEDIA — gestibile con accorgimenti, ma può invalidare le misure se non gestito.

> Mitigazione proposta: (1) Orientare il ricevitore lontano dal sole. (2) Preferire zone ombreggiate. (3) Evitare ore centrali (11-15). (4) Appesantire treppiedi contro il vento. (5) Test funzionamento prima di ogni sessione. (6) Cronometro manuale come backup. (7) Assicurarsi che il pavimento sia piano e regolare (asfalto/cemento, no ghiaia/erba).

---

## 25. Setup outdoor — pavimento irregolare altera il gait pattern
**Descrizione:** Superfici irregolari (ghiaia, erba, sampietrini) alterano il pattern del cammino e la velocità, rendendo la misura non confrontabile con norme 10MWT (validate su superfici lisce indoor).

**Gravità:** MEDIA-ALTA per confronto con dati normativi.

> Mitigazione proposta: usare tratto di asfalto o cemento liscio. Documentare sempre il tipo di superficie nel report.

---

## 23. Consegna materiale — tempistiche Amazon
**Descrizione:** Il Cronox 3.0 potrebbe non essere disponibile su Amazon.it con consegna Prime. Rischio di non ricevere il materiale entro la data prevista.

**Gravità:** BASSA — logistico, non clinico.

> Mitigazione proposta: verificare disponibilità Prime prima dell'ordine. Alternative: ordine diretto dal sito Cronox, acquisto presso negozio sportivo locale, noleggio.

---

## 26. Sample size insufficiente per lo studio di validazione
**Descrizione:** Per uno studio di agreement (Bland-Altman) e reliability (ICC) pubblicabile, COSMIN richiede minimo 50 soggetti per rating "buono" e >= 100 per "eccellente". Con meno di 30 soggetti il rating e' "scarso" e la pubblicazione potrebbe essere rifiutata. Molti studi pilota nella letteratura hanno 22-47 soggetti, che e' sufficiente solo per risultati preliminari.

**Gravita':** MEDIA-ALTA — impatta direttamente sulla pubblicabilita' dello studio.

> Mitigazione proposta: (1) Definire a priori il sample size con calcolo formale (Walter 1998 per ICC, Lu 2016 per Bland-Altman) basato sui parametri attesi. (2) Se risorse limitate, puntare a minimo 50 soggetti. (3) Considerare studio pilota con 20-30 soggetti per stimare i parametri, poi studio definitivo con sample size calcolato.

---

## 27. Assenza di dati specifici Bland-Altman per treadmill vs 10MWT overground
**Descrizione:** Non sono stati trovati studi che riportino specificamente i limiti di agreement Bland-Altman per il confronto treadmill walking speed vs 10MWT overground con fotocellule. I valori di LoA usati come riferimento provengono da studi test-retest o confronto strumenti, non dallo specifico confronto del nostro studio.

**Gravita':** MEDIA — rende difficile predefinire i limiti di agreement clinici con certezza.

> Mitigazione proposta: (1) Usare la MCID (0.10 m/s) come criterio a priori per i LoA. (2) Condurre studio pilota per stimare la SD delle differenze e calcolare i LoA attesi. (3) Discutere i limiti nel paper come limitazione se non si trovano precedenti diretti.

---

## 28. Familiarizzazione tapis roulant insufficiente — effetto apprendimento
**Descrizione:** Il cammino su tapis roulant richiede adattamento biomeccanico e percettivo. Se la familiarizzazione è troppo breve, i primi trial registrati riflettono l'adattamento anziché la SSWS reale del soggetto. La letteratura indica almeno 6-10 minuti per raggiungere un pattern stabile.

**Gravità:** MEDIA — bias sistematico verso velocità più basse nei trial su tapis roulant.

> Mitigazione proposta: 5 minuti di familiarizzazione obbligatoria (non registrata) + scartare il primo minuto di ogni trial di 2 minuti, usando solo gli ultimi 60 secondi.

---

## 29. Effetto ordine non controllato
**Descrizione:** Se tutti i soggetti fanno prima il 10MWT e poi il tapis roulant (o viceversa), l'affaticamento o la familiarizzazione con il compito potrebbero introdurre un bias sistematico nella seconda condizione.

**Gravità:** MEDIA — confondente che indebolisce la validità interna.

> Mitigazione proposta: controbilanciamento dell'ordine con randomizzazione a blocchi (metà soggetti inizia con 10MWT, metà con tapis roulant). Lista di randomizzazione preparata prima della sessione.

---

## 30. Alimentazione elettrica tapis roulant alla pista di atletica
**Descrizione:** Le piste di atletica all'aperto spesso non hanno prese di corrente accessibili. Il WalkingPad richiede alimentazione elettrica continua.

**Gravità:** MEDIA-ALTA — senza corrente, metà dello studio non può svolgersi.

> Mitigazione proposta: (1) Verificare in anticipo disponibilità prese di corrente presso la struttura. (2) Portare un generatore portatile o una batteria/power station (es. EcoFlow, Jackery) con potenza sufficiente (il WalkingPad assorbe ~500W). (3) Prolunga da esterno di almeno 25m.

---

## 31. Sicurezza soggetti su tapis roulant outdoor — assenza corrimano
**Descrizione:** Il WalkingPad è un tapis roulant compatto senza corrimano laterali. In ambiente outdoor, su superficie potenzialmente non perfettamente piana, il rischio caduta per soggetti con deficit funzionale è aumentato.

**Gravità:** ALTA — rischio caduta, soprattutto per soggetti anziani/protesizzati.

> Mitigazione proposta: (1) Posizionare il tapis roulant accanto a un supporto (tavolo robusto, ringhiera, muro). (2) Operatore sempre a portata di braccio. (3) Superficie di appoggio del tapis roulant perfettamente piana e stabile. (4) Escludere soggetti ad alto rischio caduta dal trial su tapis roulant.

---

# SEZIONE: Clinical Data Platform (Server dati pazienti)

---

## 32. GDPR e dati sanitari (Art. 9) — server centralizzato
**Descrizione:** Video e dati clinici sono dati sanitari, categoria speciale GDPR. Conservarli su un server richiede base giuridica solida (consenso esplicito o finalità di cura), DPIA obbligatoria, registro dei trattamenti.

**Gravità:** ALTA — sanzioni fino a 20M€ o 4% fatturato.

- Stato: **DA AFFRONTARE**

---

## 33. Localizzazione server — datacenter UE
**Descrizione:** Il server Hetzner deve essere in un datacenter UE (Germania/Finlandia) per compliance GDPR. Un datacenter fuori UE (USA, Singapore) richiederebbe garanzie aggiuntive.

**Gravità:** ALTA — trasferimento extra-UE non autorizzato.

- Stato: **DA VERIFICARE** (conferma datacenter Hetzner)

---

## 34. Pseudonimizzazione — tabella di raccordo
**Descrizione:** Se nome, cognome, codice fiscale finiscono sul server insieme ai dati clinici, diventa un target ad altissimo valore in caso di breach. La tabella di raccordo (ID pseudonimo ↔ identità reale) deve stare separata, idealmente offline.

**Gravità:** ALTA — data breach con dati identificativi + sanitari.

- Mitigazione pianificata: ID pseudonimizzati sul server, tabella raccordo offline/su sistema separato.
- Stato: **DA IMPLEMENTARE**

---

## 35. Video con volto = dati biometrici
**Descrizione:** Se i video mostrano il volto del paziente, diventano dati biometrici (Art. 9 GDPR), con livello di protezione ancora più elevato. Il volto NON è equivalente al nome: il nome è dato personale ordinario (Art. 6), il volto è potenzialmente dato biometrico (Art. 9, categoria speciale) con protezione rafforzata. Anche senza riconoscimento facciale, il Garante italiano tende a trattare video clinici con volto come dato sensibile.

**Gravità:** ALTA se volto visibile.

- Possibili mitigazioni: ripresa solo gambe/piedi, blur automatico del volto.
> #fix 2026-03-19: Decisione di implementare blur automatico del volto come step obbligatorio nella pipeline di upload. Sul server va SOLO la versione blurrata. Video originale resta in locale o viene cancellato dopo conferma. Tecnologia: FFmpeg + face detection model. Questo riduce drasticamente il danno in caso di breach (due layer indipendenti: pseudonimizzazione nome + blur volto).
- Stato: **MITIGAZIONE IN CORSO**

---

## 36. Consenso informato per piattaforma dati
**Descrizione:** Serve consenso specifico per: raccolta video, conservazione su server remoto, condivisione tramite link protetto, durata della conservazione, diritto alla cancellazione.

**Gravità:** ALTA — trattamento senza base giuridica valida.

- Stato: **DA CREARE** modulo consenso specifico per la piattaforma

---

## 37. Sicurezza link di condivisione
**Descrizione:** I link protetti da password possono essere inoltrati a terzi non autorizzati. La password potrebbe essere intercettata se inviata sullo stesso canale del link.

**Gravità:** MEDIA-ALTA — accesso non autorizzato ai video del paziente.

- Mitigazioni pianificate: scadenza temporale, limite accessi, IP logging, possibilità di revoca, invio password su canale separato.
- Stato: **DA IMPLEMENTARE**

---

## 38. Sicurezza server Hetzner
**Descrizione:** Server esposto su internet con dati sanitari. Target per breach, ransomware, accesso non autorizzato.

**Gravità:** ALTA.

- Mitigazioni pianificate: LUKS encryption at rest, firewall restrittivo, fail2ban, SSH key-only, aggiornamenti automatici, backup cifrati su storage separata.
- Stato: **DA IMPLEMENTARE**

---

## 39. Backup e disaster recovery
**Descrizione:** Perdita dati clinici = perdita irreversibile. Guasto hardware, errore umano, ransomware.

**Gravità:** ALTA.

- Mitigazione pianificata: backup cifrati incrementali (Restic) su Hetzner Storage Box separata.
- Stato: **DA IMPLEMENTARE**

---

## 40. DPO — necessità di un Data Protection Officer
**Descrizione:** Se il trattamento di dati sanitari è su larga scala, la nomina del DPO è obbligatoria. Anche sotto-scala, è fortemente raccomandato per dati sanitari. Con 50-100 pazienti in studio di ricerca, probabilmente NON obbligatorio (singolo professionista, non larga scala).

**Gravità:** MEDIA — non conformità GDPR.

- Stato: **DA VERIFICARE** (dipende dalla scala del trattamento)
- Azione pianificata (2026-03-19): consulenza privacy una tantum con avvocato/consulente per validare DPIA, consenso informato e confermare esenzione DPO.

---

## 41. Retention policy — durata conservazione dati
**Descrizione:** Manca una politica di conservazione: per quanto tempo si tengono i dati? La conservazione illimitata viola il principio di minimizzazione GDPR.

**Gravità:** MEDIA.

- Stato: **DA DEFINIRE**

---

## 42. BLE driver — pacchetti malformati dal WalkingPad
**Descrizione:** Il WalkingPad invia occasionalmente pacchetti BLE troncati o malformati (es. 11 byte invece dei 15 attesi per messaggi di stato). ph4-walkingpad crasha con `bytearray index out of range` (Issue #16). Questo causa perdita di connessione e interruzione del monitoraggio.

**Gravita':** ALTA — durante misurazione SSWS, perdere il monitoraggio significa perdere il trial.

> #fix 2026-03-19: Il nostro driver dovra' validare la lunghezza di ogni pacchetto PRIMA di accedere ai byte per indice. Pacchetti corti vanno ignorati con warning, non causare crash. Pattern: `if len(data) < 15: log.warning("short packet"); return None`.

---

## 43. BLE driver — WalkingPad ignora comandi troppo ravvicinati
**Descrizione:** Il WalkingPad ignora silenziosamente i comandi BLE inviati troppo rapidamente. Non c'e' errore, semplicemente il comando non ha effetto. Confermato dal codice QWalkingPad: "the WalkingPad ignores commands if they come in too quickly".

**Gravita':** MEDIA — un cambio velocita' che non va a effetto potrebbe essere un rischio per il paziente se l'operatore pensa di aver dato il comando.

> #fix 2026-03-19: Implementare coda comandi con throttling (minimo 100-200ms tra comandi). Confermare ogni cambio velocita' leggendo il prossimo pacchetto di stato. Se la velocita' riportata non corrisponde a quella comandata dopo 2 secondi, re-inviare il comando.

---

## 44. BLE driver — caratteristiche mancanti su modelli diversi
**Descrizione:** Alcuni modelli WalkingPad (es. Z1) non espongono le caratteristiche BLE standard 0xfe01/0xfe02. Il driver crasha con NoneType error se tenta di usare caratteristiche non trovate (ph4-walkingpad Issue #23).

**Gravita':** MEDIA — impatta solo se si usa un modello diverso da quello testato.

> #fix 2026-03-19: Il driver dovra' verificare l'esistenza delle caratteristiche dopo il discovery e produrre un errore chiaro ("Modello non compatibile: caratteristiche 0xfe01/0xfe02 non trovate") invece di crashare.

---

## 45. BLE driver — event loop asyncio su Python 3.10+
**Descrizione:** ph4-walkingpad ha problemi di compatibilita' asyncio su Python 3.10+ ("Task got Future attached to a different loop"). La creazione esplicita di event loop confligge con il loop gia' esistente.

**Gravita':** MEDIA — il nostro driver deve funzionare su Python moderno.

> #fix 2026-03-19: Non creare mai event loop espliciti. Usare `asyncio.get_event_loop()` o `asyncio.run()` (Python 3.7+). Testare su Python 3.10+ prima dell'uso clinico.

---

## 46. BLE driver — due protocolli KingSmith incompatibili (R1 vs R2)
**Descrizione:** L'analisi del codice sorgente di qdomyos-zwift (cagnulein/qdomyos-zwift) rivela che KingSmith usa DUE protocolli BLE completamente diversi:
- **R1 Pro (kingsmithr1protreadmill)**: pacchetti binari raw con header 0xf7, checksum semplice. UUID servizio: 0xFE00, write: 0xFE02, notify: 0xFE01.
- **R2 / X21 / G1 (kingsmithr2treadmill)**: protocollo testuale (comandi ASCII tipo "props CurrentSpeed 3.5") cifrato con tabella di sostituzione base64. UUID servizio: 0x1234, write: 0xFED7, notify: 0xFED8. **7 diverse tabelle di cifratura** a seconda del modello.

Il nostro WalkingPad potrebbe usare l'uno O l'altro protocollo. Se assumiamo il protocollo sbagliato, la comunicazione non funzionera' affatto.

**Gravita':** ALTA — potrebbe bloccare l'intero progetto se non identificato correttamente.

> #fix 2026-03-19: Documentata la differenza nel report di analisi qdomyos-zwift. Strategia: (1) Identificare il nome BLE esatto del nostro WalkingPad. (2) Verificare quale pattern di nome BLE corrisponde nella logica di detection di bluetooth.cpp. (3) Se il nome inizia con "WALKINGPAD" o "KS-ST-A1P" o "KS-H" ecc. -> protocollo R1. Se inizia con "KS-ST-K12PRO" o "KS-X21" ecc. -> protocollo R2.

---

## 47. BLE driver — UUID del servizio variano per modello KingSmith
**Descrizione:** Diversi modelli KingSmith usano UUID diversi anche all'interno dello stesso protocollo R2:
- Standard: 0x1234 / 0xFED7 / 0xFED8
- KS-NACH-X21C: prefix 0002xxxx
- KS-NGCH-G1C / KS-NACH-MXG: prefix 0001xxxx
Il codice qdomyos-zwift ha fallback automatici (se il primo UUID non viene trovato, prova il secondo).

**Gravita':** MEDIA — il driver deve tentare piu' UUID se il primo fallisce.

> #fix 2026-03-19: Adottare la stessa strategia di fallback di qdomyos-zwift nel nostro driver.

---

## 48. BLE driver — lock mode del treadmill dopo inattivita'
**Descrizione:** Il treadmill entra in lock mode dopo ~15 minuti di inattivita'. Un test clinico potrebbe essere interrotto se il treadmill si blocca tra un trial e l'altro.

**Gravita':** MEDIA — perdita trial durante sessione clinica.

> #fix 2026-03-19: qdomyos-zwift gestisce questo automaticamente: nel protocollo R1, quando riceve il byte 0x05 nella posizione 2 del pacchetto, imposta requestUnlock=true e invia il comando di unlock {0xf7, 0xa2, 0x02, 0x01, 0xa5, 0xfd}. Da implementare nel nostro driver.

---

## 49. BLE driver — target speed errata durante startup
**Descrizione:** Documentato in issue #470 di qdomyos-zwift: durante la fase di avvio, il treadmill invia target speed errate ("bugged target speed"). Il codice implementa un workaround complesso per distinguere tra target speed reale e bug.

**Gravita':** BASSA per il nostro caso — noi leggiamo solo la velocita' corrente, non la target speed.

---

## 50. BLE driver — null pointer crash su service discovery
**Descrizione:** Se il servizio BLE atteso (0xFE00 o 0x1234) non viene trovato sul dispositivo, il codice originale crashava. qdomyos-zwift ha aggiunto controllo null dopo createServiceObject(). Alcuni modelli KingSmith hanno FTMS (0x1826) invece del protocollo proprietario.

**Gravita':** MEDIA — crash del driver se il modello usa FTMS.

> #fix 2026-03-19: Il nostro driver dovra' verificare il risultato di service discovery e gestire i casi: (1) servizio atteso trovato -> OK, (2) servizio atteso non trovato ma FTMS presente -> segnalare all'utente, (3) nessun servizio compatibile -> errore chiaro.

---

## 51. Telecomando fisico — paziente preme tasti sbagliati durante il test
**Descrizione:** Il telecomando WalkingPad ha 4 tasti (Stop, Modo, +, -). Se il paziente tiene in mano il telecomando come emergency stop, potrebbe accidentalmente premere uno degli altri 3 tasti, cambiando modalità (auto/manuale) o velocità, invalidando la misura senza che l'operatore se ne accorga.

**Gravità:** MEDIA — non è un rischio di sicurezza fisica (il nastro non va più veloce del massimo impostato), ma invalida i dati della sessione.

> #fix 2026-03-19: Doppia soluzione implementata:
> (1) FISICA: proposto guscio/cover per telecomando che espone solo il tasto Stop (button guard). Realizzabile con stampa 3D, nastro isolante, o cartoncino rigido.
> (2) SOFTWARE: aggiunto rilevamento tamper nel driver (walkingpad_driver.py). Il driver monitora: (a) cambio di modalità non comandato dal software → log warning + ripristino automatico; (b) variazione di velocità anomala rispetto all'ultimo comando inviato → log warning. Gli eventi vengono segnalati via callback on_tamper e loggati. Il test viene marcato come potenzialmente invalidato.

---

# SEZIONE: Raspberry Pi come controller BLE clinico

---

## 52. Raspberry Pi BLE — BlueZ/bleak instabilità su Linux
**Descrizione:** Multipli issue documentati su GitHub (bleak #332, #1603, #1240, #1358, #1319): BleakDBusError "Operation already in progress" durante scanning, service discovery che restituisce servizi vuoti, connessioni inaffidabili che richiedono molti tentativi. Problemi più frequenti su RPi che su laptop. BlueZ su Linux ha supporto BLE meno maturo rispetto a macOS/Windows.

**Gravità:** MEDIA-ALTA — in contesto clinico, una connessione BLE inaffidabile può invalidare trial o ritardare le sessioni.

> Mitigazione proposta: (1) Usare BlueZ >= 5.55 (meglio 5.66+). (2) Aggiornare a Raspberry Pi OS Bookworm (BlueZ 5.66). (3) Implementare retry robusto con backoff esponenziale nella logica di connessione. (4) Power cycle del Bluetooth adapter (`sudo hciconfig hci0 reset`) come fallback automatico. (5) Testare approfonditamente la stabilità BLE col WalkingPad specifico PRIMA dell'uso clinico.

---

## 53. Raspberry Pi BLE — antenna condivisa Wi-Fi/Bluetooth (interferenza 2.4 GHz)
**Descrizione:** Tutti i modelli Raspberry Pi (3, 4, 5) usano il chipset CYW43455 che condivide la stessa antenna per Wi-Fi 2.4 GHz e Bluetooth. Il traffico Wi-Fi intenso sulla banda 2.4 GHz può degradare le prestazioni BLE. In ambiente ospedaliero ci possono essere molti access point Wi-Fi e dispositivi medicali che interferiscono sulla banda 2.4 GHz.

**Gravità:** MEDIA — potrebbe causare disconnessioni BLE sporadiche durante la sessione.

> Mitigazione proposta: (1) Configurare il Wi-Fi del Pi sulla banda 5 GHz (supportata da Pi 4 e 5), liberando la banda 2.4 GHz per il BLE. (2) Se la rete ospedaliera è solo 2.4 GHz, usare un dongle USB Wi-Fi per la rete e lasciare l'antenna interna al BLE. (3) Posizionare il Pi entro 2-3 metri dal WalkingPad.

---

## 54. Raspberry Pi — affidabilità scheda microSD in uso continuativo
**Descrizione:** Le schede microSD hanno un numero limitato di cicli di scrittura. Il logging continuo, i file temporanei di Flask, e il journaling del filesystem possono consumare la SD rapidamente. Corruzione della SD = sistema non avviabile.

**Gravità:** MEDIA-ALTA — in contesto clinico, un dispositivo che non si avvia il giorno della sessione è inaccettabile.

> Mitigazione proposta: (1) Usare schede microSD di qualità industriale (Samsung PRO Endurance, SanDisk MAX Endurance). (2) Montare /tmp e /var/log come tmpfs (in RAM) per ridurre scritture su SD. (3) Avere una SD di backup con immagine clonata pronta. (4) Valutare boot da USB SSD (supportato nativamente su Pi 4 e 5) per maggiore affidabilità.

---

## 55. Raspberry Pi — alimentazione insufficiente causa instabilità
**Descrizione:** Il Raspberry Pi è sensibile all'alimentazione. Un alimentatore sotto-dimensionato causa throttling della CPU, instabilità del Bluetooth, e crash random. Il Pi 4 richiede 5V/3A (USB-C), il Pi 5 richiede 5V/5A (27W USB-C). Alimentatori generici o cavi USB economici possono non fornire corrente sufficiente.

**Gravità:** MEDIA — instabilità intermittente difficile da diagnosticare.

> Mitigazione proposta: usare SOLO l'alimentatore ufficiale Raspberry Pi. Per il Pi 5: alimentatore ufficiale da 27W. Mai usare hub USB o caricatori per telefono.

---

## 56. Raspberry Pi — sicurezza rete in ambiente ospedaliero
**Descrizione:** Il Pi espone un web server Flask sulla rete locale. In ambiente ospedaliero, la rete potrebbe essere condivisa con altri dispositivi. Un server Flask non protetto è accessibile da chiunque sulla stessa rete.

**Gravità:** MEDIA — accesso non autorizzato al controllo del tapis roulant.

> Mitigazione proposta: (1) Usare una rete Wi-Fi dedicata/isolata (hotspot dal telefono o access point dedicato). (2) Implementare autenticazione nel server Flask. (3) Firewall sul Pi (ufw) per accettare connessioni solo da IP specifici. (4) HTTPS con certificato self-signed.

---

## 57. Server web — MODE_MANUAL causava arresto immediato del nastro
**Descrizione:** Il server impostava MODE_MANUAL e poi tentava di controllare la velocità via software usando `app_speed_raw` (lettura sensore piede) come target. In modalità manuale, il sensore piede restituisce 0 se nessuno è sul pad o valori instabili. Il loop di controllo velocità riduceva la velocità a 0 in ~6 secondi, fermando il nastro.

**Gravità:** ALTA — rendeva il sistema inutilizzabile per la misurazione SSWS.

> #fix 2026-03-19: Cambiato da MODE_MANUAL a MODE_AUTO in walkingpad_server.py. Rimossa tutta la logica di controllo velocità software (rampa, rate limiting, app_speed tracking). In MODE_AUTO il WalkingPad gestisce la velocità autonomamente in base al sensore piede, che è esattamente il comportamento necessario per misurare la SSWS (velocità autodeterminata). Il server ora si limita a monitorare.

---

# SEZIONE: Integrazione WalkingPad → Server Clinico (API)

---

## 58. API token esposto nel browser — rischio furto credenziali
**Descrizione:** Se il token API venisse incluso nel JavaScript del browser (fetch diretta dal browser al server clinico), chiunque ispezioni il codice sorgente della pagina potrebbe rubarlo e fare richieste non autorizzate al server clinico.

**Gravità:** ALTA — accesso non autorizzato ai dati clinici di tutti i pazienti.

> #fix 2026-03-19: Implementato proxy server-side. Il Flask server (walkingpad_server.py) agisce da proxy: il browser chiama localhost:5050/send_to_server, il Flask server aggiunge i token e chiama i server remoti. I token non sono mai esposti al browser.

---

## 59. Nomi pazienti in transito verso il server clinico
**Descrizione:** Se il nome del paziente transitasse dal Flask al server clinico, violerebbe il principio di separazione della pseudonimizzazione (i nomi devono stare solo sul vault, i dati clinici solo sul server clinico).

**Gravità:** ALTA — viola architettura GDPR a due server.

> #fix 2026-03-19: Implementato flusso a due fasi: (1) Flask chiama vault.3d-ga.it con nome+cognome+CF → riceve pseudo_id, (2) Flask chiama 3d-ga.it con solo pseudo_id + dati clinici. Il server clinico non vede MAI i nomi reali.

---

## 60. Invio dati su HTTP non cifrato
**Descrizione:** Se i server non hanno ancora HTTPS attivo (in attesa propagazione DNS), i token API e i dati clinici transiterebbero in chiaro sulla rete.

**Gravità:** ALTA — intercettazione token e dati clinici.

> #fix 2026-03-19: Aggiunto controllo nel Flask server che rifiuta l'invio a URL non HTTPS (eccetto localhost per sviluppo). Il codice verifica `url.startswith("https://")` prima di ogni POST.

---

## 61. Duplicazione sessioni per doppio click
**Descrizione:** Se l'operatore clicca due volte "Invia al server clinico", potrebbero crearsi due ClinicalTest duplicati per la stessa sessione.

**Gravità:** BASSA — non è un rischio di sicurezza, ma corrompe i dati.

> #fix 2026-03-19: Implementata idempotency key. Ad ogni sessione viene generato un UUID univoco (session_uuid). Il server clinico controlla se esiste già un ClinicalTest con quel session_uuid in extra_data e restituisce "already_exists" invece di creare un duplicato.

---

## 62. Rete clinica non disponibile — perdita dati sessione
**Descrizione:** Se la rete è assente o instabile al momento dell'invio (es. Wi-Fi della clinica giù), i dati della sessione non vengono salvati sul server. Il CSV locale è l'unico backup.

**Gravità:** MEDIA — sessione persa se l'operatore non scarica il CSV e il browser viene chiuso.

> Mitigazione parziale: il CSV rimane scaricabile localmente. Possibile miglioramento futuro: coda di upload locale (salvare payload su disco e ritentare al prossimo avvio server).

---

## 63. Token API compromesso — necessità di revoca rapida
**Descrizione:** Se il laptop della clinica viene rubato, il token API salvato in `.clinical_api_token` è compromesso. Finché il token è attivo, chi lo possiede può inviare dati al server clinico.

**Gravità:** MEDIA-ALTA — accesso in scrittura ai dati clinici.

> #fix 2026-03-19: Implementato modello APIToken nel Django admin con campo `is_active` e azione batch "Disattiva token". L'admin può disattivare un token compromesso in 10 secondi dal pannello Django. Il campo `last_used_at` permette di verificare se il token è stato usato dopo il furto.

---

## 64. Codice fiscale come identificativo — limiti e rischi
**Descrizione:** Il codice fiscale è usato come chiave primaria per l'identity matching. Problemi potenziali: (1) CF omocodia (due persone con lo stesso CF), (2) CF errato inserito dall'operatore, (3) CF non disponibile (paziente straniero senza CF italiano).

**Gravità:** MEDIA — paziente associato ai dati di un altro, o impossibilità di usare il sistema per pazienti stranieri.

> Mitigazione parziale: il vault ha UNIQUE constraint sul CF, quindi un CF duplicato restituisce il paziente esistente (non ne crea uno nuovo). Per pazienti stranieri, servirà un identificativo alternativo (passaporto, codice interno clinica). Da gestire in futuro.

---

## 65. CORS — superficie di attacco per richieste cross-origin
**Descrizione:** Il server clinico accetta richieste CORS da localhost:5050. In teoria, qualsiasi pagina web aperta sul Mac dell'operatore potrebbe tentare richieste cross-origin a 3d-ga.it se conosce il token.

**Gravità:** BASSA — il token è server-side (non nel browser), quindi il CORS è rilevante solo per richieste dirette dal browser, che non contengono il token. Il Bearer token è la vera barriera di sicurezza.

---

## 66. WalkingPad MODE_AUTO — decelerazione a gradino (on/off)
**Descrizione:** In MODE_AUTO, il sensore piede del WalkingPad ha un comportamento quasi binario: rileva "qualcuno cammina" o "nessuno". Non c'è una gradazione proporzionale alla posizione sul nastro. Quando il paziente si porta indietro per rallentare, non succede quasi niente, poi il nastro si ferma di colpo. Questo rende difficile modulare la velocità e crea un rischio comfort/sicurezza.

**Gravità:** MEDIA — non impatta la misurazione SSWS (la zona stabile è quella che conta), ma impatta il comfort e potenzialmente la sicurezza del paziente durante le fasi di arresto.

> Stato: PROBLEMA HARDWARE — il sensore piede del WalkingPad non è progettato per una modulazione fine. Possibili mitigazioni future: (1) ibrido AUTO+MANUAL dove il software intercetta la fase di decelerazione e la rende graduale, (2) protocollo operativo: l'esaminatore comanda lo stop dalla UI quando la misurazione è completa, il paziente si porta ai lati del nastro.

---

## 67. Auto-detect SSWS — selezionava zone a velocità nulla
**Descrizione:** L'algoritmo automatico per stimare la SSWS cercava la finestra con minor deviazione standard, senza vincoli su quale parte della prova. Selezionava zone a 0.3 km/h (paziente quasi fermo) invece della vera velocità di crociera.

**Gravità:** MEDIA — dato SSWS completamente errato se l'esaminatore non segna manualmente.

> #fix 2026-03-19: Algoritmo riscritto con 3 criteri: (1) scarta primo e ultimo 20% della durata (fasi transitorie), (2) solo punti con velocità >= 50% del picco raggiunto, (3) finestra di 15s con minor SD tra quelle rimaste. Questo garantisce che la SSWS venga dalla zona centrale a velocità di crociera.

---

## 68. Compatibilità driver BLE con modelli WalkingPad diversi — assenza di verifica pre-uso
**Descrizione:** Se si usa il driver con un WalkingPad diverso da quello testato (modello diverso, firmware aggiornato, o treadmill di altra marca), non c'è modo di sapere in anticipo se il protocollo è compatibile. Un fallimento silenzioso (comandi ignorati, pacchetti non parsabili) potrebbe essere scambiato per un malfunzionamento del dispositivo, causando perdita di tempo in sessione clinica.

**Gravità:** MEDIA — ritardo operativo e possibile impossibilità di effettuare la misurazione.

> #fix 2026-03-12: Creato `walkingpad_compat_check.py` — script di verifica compatibilità in modalità SOLO LETTURA (non invia mai comandi di movimento). Esegue 13 check in sequenza: connessione BLE, servizio 0xFE00, caratteristiche 0xFE01/0xFE02, sottoscrizione notifiche, profile handshake, status query, formato pacchetto, parsing stato, valori plausibili, query parametri, nome dispositivo, mappa servizi completa. Produce un report PASS/FAIL/WARN con dettaglio per ogni check. Exit code 0 = compatibile, 1 = non compatibile. Uso: `python walkingpad_compat_check.py` (scansione automatica) o `python walkingpad_compat_check.py <indirizzo>`.
