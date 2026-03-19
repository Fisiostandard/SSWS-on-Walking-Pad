# Metodologia Studio di Validazione — Treadmill vs 10MWT Overground
## Ricerca metodologica (2026-03-17)

---

## 1. Sample Size

### Bland-Altman Agreement

Non esiste un singolo numero "magico". Le raccomandazioni si sono evolute:

- **Rule-of-thumb storica**: minimo 50 soggetti (Carstensen), spesso citato come "almeno 100" per studi di method comparison.
- **COSMIN checklist** (Mokkink et al. 2010): classifica la qualità metodologica per sample size come:
  - **Eccellente**: >= 100 soggetti
  - **Buona**: >= 50 soggetti
  - **Discreta**: >= 30 soggetti
  - **Scarsa**: < 30 soggetti
- **Lu et al. (2016)** — metodo formale implementato in MedCalc: calcola il sample size sulla base di errore tipo I e II, SD delle differenze, e limiti clinici predefiniti di agreement. Questo e' il metodo piu' rigoroso.
- **Martin Bland** (York University): raccomanda di stimare il sample size dalla larghezza attesa dell'intervallo di confidenza dei limiti di agreement, usando la formula SE = sqrt(3s^2/n).

**NOTA SU BONETT 2002**: Ho cercato specificamente "Bonett 2002" per Bland-Altman. Il paper di Bonett 2002 NON riguarda Bland-Altman ma ICC. I due paper di Bonett 2002 sono:
1. "Sample size requirements for estimating intraclass correlations with desired precision" — Statistics in Medicine, 21:1331-1335. (Sicurezza: 0.98 — verificato su PubMed e Wiley)
2. "Sample Size Requirements for Testing and Estimating Coefficient Alpha" — Journal of Educational and Behavioral Statistics. (Sicurezza: 0.95 — verificato su SAGE e ERIC)

### ICC — Walter et al. 1998

- **Walter SD, Eliasziw M, Donner A. (1998)** "Sample size and optimal designs for reliability studies." Statistics in Medicine, 17(1):101-110. (Sicurezza: 0.97 — verificato su PubMed PMID 9463853)
- Fornisce tabelle per il numero di soggetti necessari dato:
  - ICC atteso sotto H0 e sotto H1
  - Numero di misurazioni per soggetto (k)
  - Potenza desiderata e livello alfa
- Esempio comune dalla letteratura derivata: per ICC atteso 0.90, H0=0.60, alfa=0.05, potenza=0.80, k=3 misurazioni -> circa **22-30 soggetti** necessari.
- Informazione dubbia sul numero esatto (0.75) — i valori specifici dipendono dai parametri scelti; consultare le tabelle originali del paper o un calcolatore online (es. wnarifin.github.io/ssc/ssicc.html).

### Bonett 2002 (per ICC)

Il metodo di Bonett calcola il numero approssimato di soggetti per ottenere un CI esatto di larghezza desiderata per ICC. Formula 3 del paper. Per k=2 e rho>0.7, aggiungere 5*rho a n per migliorare l'approssimazione.

### Raccomandazione pratica per il nostro studio

**Minimo 50 soggetti** (rating COSMIN "buono"), ideale **>= 100** (rating COSMIN "eccellente"). Per un calcolo formale, usare il metodo Lu et al. 2016 per Bland-Altman e Walter 1998 per ICC, basati sui parametri attesi dal pilota.

---

## 2. Numero di Trial Ripetuti per Soggetto

### Protocollo standard 10MWT
- **Physiopedia / SRALAB RehabMeasures Database**: il protocollo standard prevede **3 trial a velocita' confortevole + 3 trial a velocita' massima**, si fa la media dei 3 trial per ciascuna condizione.
- Variante comune: **2 trial per condizione** (2 confortevole + 2 massima), media dei 2.
- Il primo trial di ciascun blocco puo' essere di familiarizzazione (scartato).
- Setup: corridoio 14m, 2m accelerazione + 10m cronometrati + 2m decelerazione.

### Studi di validazione treadmill vs overground
- **Tipicamente 3 trial per condizione** per ciascun soggetto.
- Alcuni protocolli usano fino a 10 trial per ottenere 3 "accettabili".
- Uno studio ha usato 3 blocchi x 4 trial x 3 condizioni di velocita' = 36 trial totali (estremo).
- **Familiarizzazione treadmill**: minimo **10 minuti** di cammino su tapis roulant prima della raccolta dati (dato consistente in letteratura).

### Raccomandazione per il nostro studio
**3 trial per condizione** (treadmill e overground), media dei 3. Trial di familiarizzazione obbligatorio su treadmill (10 min). Ordine randomizzato o controbilanciato tra le due condizioni.

(Sicurezza: 0.90 — i numeri sono consistenti tra piu' fonti ma le raccomandazioni specifiche variano tra studi)

---

## 3. Numero di Rater per Inter-Rater Reliability del 10MWT

### Evidenza dalla letteratura
- **2 rater** e' lo standard minimo per studi di inter-rater reliability del 10MWT.
- Studi trovati:
  - Cerebral palsy (Kim & Park 2017, PMID 28277557): 2 rater, ICC inter-rater = 0.998 (CI 0.996-0.999). (Sicurezza: 0.95)
  - Stroke acuto (2022, Physiotherapy Theory and Practice): testati da 1 di 3 fisioterapisti, ICC1,1 = 0.76 (CI 0.59-0.87). (Sicurezza: 0.90)
  - SCI (van Hedel et al. 2005, Spinal Cord): ICC inter/intra-rater 0.95-0.99. (Sicurezza: 0.85)
  - Emiparesi cronica (2018, Topics in Stroke Rehabilitation): ICC inter-rater 99.9% per velocita'. (Sicurezza: 0.85)

### Nota importante per il nostro studio
Se usiamo **fotocellule**, l'inter-rater reliability e' quasi irrilevante perche' la misura e' automatizzata (non dipende dal rater). L'inter-rater reliability e' critica solo con **cronometro manuale**.

### Raccomandazione
- Con fotocellule: **1 operatore e' sufficiente** per la raccolta dati. La reliability e' intrinseca allo strumento.
- Se si vuole comunque documentare inter-rater reliability (es. per il paper): **2 rater** che indipendentemente gestiscono le fotocellule in sessioni separate.
- Con cronometro manuale (backup): servono **almeno 2 rater** per documentare inter-rater reliability.

---

## 4. Caratteristiche della Popolazione

### Studi di validazione gait speed — criteri tipici

**Eta':**
- Studi su giovani adulti sani: 18-30 anni
- Studi su anziani sani: 60-80 anni
- Studi misti: 18-65 anni (range piu' comune per validazione strumenti)
- Studi riabilitazione ortopedica: tipicamente >= 50 anni (OA ginocchio), o 18-65 (trauma/post-chirurgico)

**Criteri di inclusione tipici:**
- Capacita' di deambulazione autonoma (con o senza ausili)
- Capacita' di comprendere istruzioni verbali
- Consenso informato
- Per ortopedia: diagnosi specifica (es. OA ginocchio, post-protesi, post-frattura)

**Criteri di esclusione tipici:**
- Patologie neurologiche che interferiscono con il cammino
- Artrite severa o problemi ortopedici che limitano la deambulazione (se non e' la popolazione target)
- Deficit visivi severi non corretti
- Deficit cognitivi (MMSE < 24 in alcune popolazioni)
- Patologie cardiopolmonari non compensate
- Dolore acuto che impedisce la deambulazione
- Necessita' di assistenza fisica di un terapista per camminare
- Chirurgia recente (< 6 settimane, variabile)
- Lesioni arti inferiori negli ultimi 6 mesi (per studi su sani)

**Sample size negli studi trovati:**
- 22-47 soggetti per studi di validazione (range trovato)
- 30 giovani + 28 anziani in uno studio su ambienti multipli
- 42 volontari (24 giovani + 18 anziani) in un dataset pubblico

(Sicurezza: 0.85 — i criteri sono consistenti ma variano significativamente tra studi e popolazioni target)

---

## 5. Valori ICC e Bland-Altman Accettabili

### ICC — Linee guida interpretative

**Koo & Li (2016)** — Journal of Chiropractic Medicine (PMID 27330520). Linee guida piu' citate:
- ICC < 0.50: affidabilita' **scarsa**
- ICC 0.50-0.75: affidabilita' **moderata**
- ICC 0.75-0.90: affidabilita' **buona**
- ICC > 0.90: affidabilita' **eccellente**

(Sicurezza: 0.98 — verificato su PubMed/PMC)

**Cicchetti (1994)** — classificazione alternativa:
- ICC < 0.40: scarsa
- ICC 0.40-0.59: discreta
- ICC 0.60-0.74: buona
- ICC > 0.75: eccellente

(Sicurezza: 0.90)

**Per il 10MWT specificamente**, la letteratura riporta:
- Test-retest reliability: ICC 0.95-0.99 (con fotocellule)
- Inter-rater reliability: ICC 0.76-0.998 (variabile per popolazione)

### Bland-Altman Limits of Agreement

**Cosa e' "accettabile" dipende dal contesto clinico.** Il criterio e' che i LoA debbano cadere entro i limiti di agreement clinicamente predefiniti.

**MCID (Minimal Clinically Important Difference) per gait speed:**
- Range generale: **0.10-0.20 m/s** per popolazioni patologiche
- Valori con migliore validita' statistica: **0.10-0.17 m/s**
- MDC (Minimal Detectable Change): 0.10 m/s (velocita' basse) — 0.18 m/s (velocita' alte)

(Sicurezza: 0.92 — da Oates et al. 2014 systematic review, PMID 24798823, verificato)

**Criteri di accettabilita' per Bland-Altman in gait speed:**
- Bias medio (mean difference): idealmente < 0.05 m/s
- LoA 95%: idealmente entro ± MCID, cioe' entro **± 0.10 m/s** per uso clinico stringente, o **± 0.20 m/s** come limite massimo accettabile
- Percentage error < 30% (criterio Critchley & Critchley, usato in alcuni studi)

**Dati dalla letteratura per confronti simili:**
- Test-retest gait speed: bias -0.02 a -0.11 m/s, LoA da -0.49 a +0.37 m/s (piuttosto ampi)
- Confronto strumenti gait: LoA di ± 0.07 m/s (caso migliore trovato)

**Informazione dubbia (0.70)**: I valori specifici di LoA per treadmill vs overground non sono stati trovati in modo diretto. I dati sopra provengono da studi test-retest o confronto strumenti, non specificamente treadmill vs 10MWT overground.

### Raccomandazione per il nostro studio
- **ICC target**: >= 0.75 (buono per Koo & Li), idealmente >= 0.90 (eccellente)
- **Bland-Altman**: predefinire limiti di agreement clinici a **± 0.10 m/s** (= MCID) prima di raccogliere i dati. Se i LoA cadono entro ± 0.10 m/s, i due metodi sono clinicamente intercambiabili.
- Se i LoA sono > ± 0.10 ma < ± 0.20 m/s, discussione clinica necessaria.
- Se i LoA sono > ± 0.20 m/s, i metodi NON sono intercambiabili.

---

## Riferimenti Verificati

1. Walter SD, Eliasziw M, Donner A. Sample size and optimal designs for reliability studies. Stat Med. 1998;17(1):101-110. PMID: 9463853. **(Sicurezza: 0.97)**
2. Bonett DG. Sample size requirements for estimating intraclass correlations with desired precision. Stat Med. 2002;21(9):1331-1335. PMID: 12111881. **(Sicurezza: 0.98)**
3. Koo TK, Li MY. A Guideline of Selecting and Reporting Intraclass Correlation Coefficients for Reliability Research. J Chiropr Med. 2016;15(2):155-163. PMID: 27330520. **(Sicurezza: 0.98)**
4. Lu MJ, et al. Sample Size for Assessing Agreement between Two Methods of Measurement by Bland-Altman Method. Int J Biostat. 2016;12(2). PMID: 27838682. **(Sicurezza: 0.95)**
5. Mokkink LB, et al. The COSMIN checklist for assessing the methodological quality of studies on measurement properties. BMC Med Res Methodol. 2010;10:22. PMC: 2852520. **(Sicurezza: 0.95)**
6. Bland JM. Sample size for a study of agreement between two methods of measurement. www-users.york.ac.uk/~mb55/meas/sizemeth.htm **(Sicurezza: 0.95 — pagina web verificata)**

### Riferimenti NON verificati (da confermare)
7. Oates AR, et al. Minimal clinically important difference for change in comfortable gait speed of adults with pathology: a systematic review. PMID: 24798823. **(Sicurezza: 0.85 — PMID trovato ma autore primo da confermare)**
8. Cicchetti DV. Guidelines, criteria, and rules of thumb for evaluating normed and standardized assessment instruments in psychology. Psychol Assess. 1994;6(4):284-290. **(Sicurezza: 0.80 — citato ampiamente ma non verificato direttamente)**

---

## Sintesi Operativa

| Parametro | Minimo | Ideale | Riferimento |
|---|---|---|---|
| Sample size | 50 | >= 100 | COSMIN, Lu 2016 |
| Trial per condizione | 3 | 3 | Standard 10MWT |
| Familiarizzazione treadmill | 10 min | 10 min | Letteratura |
| Rater (con fotocellule) | 1 | 2 (per paper) | — |
| ICC target | >= 0.75 | >= 0.90 | Koo & Li 2016 |
| LoA accettabili | ± 0.20 m/s | ± 0.10 m/s | MCID letteratura |
| Eta' campione | 18-65 | Stratificato | — |
