# Protocollo di Validazione: Tapis Roulant Self-Paced vs 10MWT con Fotocellule

**Versione:** 1.0 — 2026-03-17
**Obiettivo:** Valutare la validità concorrente (concurrent validity) e l'agreement tra la velocità di cammino autodeterminata (SSWS) misurata su tapis roulant Kingsmith WalkingPad modificato e il 10-Meter Walk Test (10MWT) con fotocellule.

---

## 1. Design dello studio

**Tipo:** Studio di agreement cross-sectional, single-session.
**Analisi principali:**
- ICC (two-way mixed, absolute agreement, single measures) tra le due misure
- Bland-Altman plot con limiti di agreement (LoA)
- Paired t-test / Wilcoxon per bias sistematico

**Target di accettabilità:**
- ICC ≥ 0.75 (buono), idealmente ≥ 0.90 (eccellente) — Koo & Li 2016
- LoA entro ± 0.10 m/s (= MCID della gait speed) per intercambiabilità clinica

---

## 2. Campione

### Numerosità
| Livello | N soggetti | Giustificazione |
|---------|-----------|-----------------|
| **Minimo accettabile** | 30 | Walter 1998: n≈22-30 per ICC atteso 0.90 con k=3, potenza 0.80 |
| **Raccomandato** | 50 | COSMIN: rating "buono" per studi di validità |
| **Ideale** | ≥100 | COSMIN: rating "eccellente" |

**Raccomandazione pratica:** puntare a **50 soggetti**, con un minimo assoluto di 30 se i vincoli logistici sono stringenti.

### Popolazione target
Dato che il tapis roulant è pensato per ambito ortopedico riabilitativo:

**Criteri di inclusione:**
- Età 40-80 anni (range rappresentativo per protesi anca/ginocchio, artrosi)
- Deambulazione autonoma (con o senza ausilio)
- Capacità di comprendere e seguire istruzioni verbali
- Consenso informato firmato

**Criteri di esclusione:**
- Patologie neurologiche (stroke, Parkinson, SM, lesioni midollari)
- Deficit visivi o cognitivi severi che impediscano la collaborazione
- Dolore acuto che impedisca la deambulazione
- Chirurgia ortopedica < 6 settimane
- Condizioni cardiovascolari instabili
- Impossibilità di camminare per almeno 2 minuti consecutivi

**Stratificazione consigliata:**
Per avere un range ampio di velocità (migliora la potenza statistica), reclutare circa:
- 1/3 soggetti sani (controlli, velocità "normali")
- 1/3 soggetti con artrosi/problemi ortopedici lievi-moderati
- 1/3 soggetti con protesi articolare o deficit funzionale significativo

---

## 3. Misurazioni per soggetto

### 10MWT (Gold Standard)
- **Corridoio:** 14 metri totali (2m accelerazione + 10m cronometrati + 2m decelerazione)
- **Fotocellule:** posizionate a inizio e fine dei 10m centrali
- **Trial:** 3 trial a velocità autodeterminata ("cammini alla sua velocità abituale")
- **Riposo:** 30 secondi tra i trial (o a richiesta del soggetto)
- **Valore registrato:** tempo in secondi per ciascun trial → velocità m/s

### Tapis roulant (strumento in validazione)
- **Familiarizzazione:** minimo 5 minuti di cammino libero sul tapis roulant (NON registrato)
- **Trial:** 3 trial di 2 minuti ciascuno in modalità self-paced
- **Pausa:** 1 minuto tra i trial
- **Valore registrato:** velocità media degli ultimi 60 secondi di ciascun trial (scartare il primo minuto come periodo di adattamento)

### Ordine
- **Controbilanciamento:** metà dei soggetti inizia con 10MWT, metà con tapis roulant (randomizzazione a blocchi)
- **Pausa tra le due condizioni:** 5 minuti di riposo seduto

### Riepilogo per soggetto
| Fase | Durata stimata |
|------|---------------|
| Accoglienza, consenso, dati demografici | 5 min |
| Familiarizzazione tapis roulant | 5 min |
| Condizione A (3 trial) | 8-10 min |
| Pausa | 5 min |
| Condizione B (3 trial) | 8-10 min |
| **Totale per soggetto** | **~35 min** |

---

## 4. Operatori

### Quanti operatori servono?

**Per il 10MWT con fotocellule:** la misura è automatizzata (il tempo lo registra la fotocellula), quindi **1 operatore basta** per la raccolta dati. La variabilità inter-operatore è trascurabile perché non c'è cronometraggio manuale.

**Per il tapis roulant:** idem, la velocità è letta dal dispositivo.

**Tuttavia**, per il paper è utile avere **2 operatori** che:
1. Gestiscano indipendentemente i comandi di start/stop del tapis roulant
2. Registrino indipendentemente i dati di velocità dal display
3. Monitorino il protocollo (istruzioni verbali standardizzate, sicurezza del soggetto)

Questo permette di calcolare anche l'**affidabilità inter-operatore** (ICC inter-rater), che rafforza il paper senza costo aggiuntivo significativo.

**Raccomandazione: 2 operatori.**

---

## 5. Analisi statistica prevista

1. **Statistiche descrittive:** media, DS, mediana, range per ciascuna condizione
2. **ICC (3,1):** two-way mixed model, absolute agreement, single measures — con IC 95%
3. **Bland-Altman:** bias medio (differenza media tra tapis roulant e 10MWT), LoA (± 1.96 × DS delle differenze), plot
4. **Test per bias sistematico:** paired t-test (o Wilcoxon se non normali)
5. **SEM e MDC:** Standard Error of Measurement e Minimal Detectable Change
6. **Regressione proporzionale:** verificare se il bias varia con il livello di velocità (Bland-Altman con regressione)

---

## 6. Piano logistico — Sabato pomeriggio alla pista di atletica

### Setup pista

```
[ZONA A: 10MWT]                          [ZONA B: TAPIS ROULANT]

|--2m--|------10m------|--2m--|           Tavolo con tapis roulant
START   FOTO1    FOTO2  STOP             + presa corrente/generatore
        ↓        ↓                       + tappetino antiscivolo
        📷       📷                      + sedia per riposo
                                          + sedia per osservazione
Superficie: corsia interna pista         Superficie: zona piana,
(asfalto/tartan, regolare)               ombreggiata se possibile
```

### Materiale necessario
- [ ] Tapis roulant Kingsmith WalkingPad + alimentazione (prolunga o generatore)
- [ ] 2 fotocellule + cavalletti
- [ ] Nastro adesivo + metro per segnare i 14m
- [ ] Coni segnaposto
- [ ] Sedia per riposo soggetti
- [ ] Tavolo per registrazione
- [ ] 2 laptop/tablet per registrazione dati (uno per operatore)
- [ ] Moduli consenso informato stampati
- [ ] Scheda raccolta dati stampata (backup cartaceo)
- [ ] Acqua per i soggetti
- [ ] Kit primo soccorso base
- [ ] Cronometro di backup (in caso guasto fotocellule)
- [ ] Lista randomizzazione ordine (preparata prima con blocchi di 4)

### Timeline sabato pomeriggio

**Pre-sessione (13:00 - 14:00)**
- Arrivo, setup pista (fotocellule, segnaletica 14m)
- Setup tapis roulant, test funzionamento
- Calibrazione fotocellule
- Briefing operatori (istruzioni standardizzate)

**Sessione 1 (14:00 - 16:30) — ~4 soggetti/ora**
- Slot da 40 minuti per soggetto (35 min test + 5 min buffer)
- Soggetti 1-10

**Pausa (16:30 - 16:45)**

**Sessione 2 (16:45 - 18:45) — ~4 soggetti/ora**
- Soggetti 11-18

**Chiusura (18:45 - 19:15)**
- Smontaggio
- Backup dati
- Verifica completezza dati

### Throughput realistico
Con 2 operatori in parallelo (uno gestisce la zona 10MWT, l'altro il tapis roulant, poi si scambiano):

| Scenario | Soggetti/ora | Tot sabato (4.5h utili) |
|----------|-------------|------------------------|
| Sequenziale (1 soggetto alla volta) | ~4 | **18** |
| Parzialmente parallelo (overlap fasi) | ~5 | **22-23** |

**Per raggiungere N=50:** servono **3 sessioni** da un sabato pomeriggio (o 2 giornate intere).

**Per il minimo N=30:** servono **2 sessioni** da un sabato pomeriggio.

---

## 7. Scheda raccolta dati (template)

| Campo | Valore |
|-------|--------|
| **ID soggetto** | ___ |
| **Data** | ___/___/2026 |
| **Operatore 1** | ___ |
| **Operatore 2** | ___ |
| **Età** | ___ anni |
| **Sesso** | M / F |
| **Altezza** | ___ cm |
| **Peso** | ___ kg |
| **Condizione ortopedica** | Sano / Artrosi / Protesi / Altro: ___ |
| **Ausilio per deambulazione** | Nessuno / Bastone / Stampella / Deambulatore |
| **Ordine randomizzato** | 10MWT prima / Tapis roulant prima |

### 10MWT
| Trial | Tempo (s) | Velocità (m/s) | Note |
|-------|----------|----------------|------|
| 1 | | | |
| 2 | | | |
| 3 | | | |
| **Media** | | | |

### Tapis roulant
| Trial | Velocità media ultimi 60s (m/s) | Op.1 | Op.2 | Note |
|-------|--------------------------------|------|------|------|
| 1 | | | | |
| 2 | | | | |
| 3 | | | | |
| **Media** | | | | |

---

## 8. Considerazioni etiche

- Approvazione comitato etico (se necessaria per la sede di ricerca)
- Consenso informato scritto
- Possibilità di interrompere in qualsiasi momento
- Nessun rischio aggiuntivo rispetto alla normale deambulazione
- Dati pseudonimizzati (ID numerico, no nomi nei file dati)
- Privacy: GDPR compliance per conservazione dati

---

## Riferimenti metodologici chiave

- Koo TJ, Li MY. *A Guideline of Selecting and Reporting Intraclass Correlation Coefficients for Reliability Research.* J Chiropr Med. 2016;15(2):155-163. PMID: 27330520
- Walter SD et al. *Sample size and optimal designs for reliability studies.* Stat Med. 1998;17(1):101-110. PMID: 9463853
- Mokkink LB et al. *The COSMIN checklist for assessing the methodological quality of studies on measurement properties.* BMC Med Res Methodol. 2010;10:22. PMID: 20298572
- Lu MJ et al. *Sample Size for Assessing Agreement between Two Methods of Measurement by Bland-Altman Method.* Int J Biostat. 2016;12(2). PMID: 27838682
