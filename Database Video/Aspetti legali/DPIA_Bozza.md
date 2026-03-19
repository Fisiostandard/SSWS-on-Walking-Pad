# DPIA — Data Protection Impact Assessment
## Piattaforma Clinical Data Platform — Progetto SSWS Misura

**Versione:** BOZZA v0.1 — da sottoporre a consulente privacy
**Data:** 2026-03-19
**Titolare del trattamento:** [NOME / STUDIO / ENTE — da compilare]
**Responsabile della redazione:** [da compilare]

---

## 1. Descrizione del trattamento

### 1.1 Natura del trattamento
Raccolta, conservazione e condivisione di dati clinici e video relativi a pazienti sottoposti a valutazione della capacità di deambulazione (Self-Selected Walking Speed e altri test funzionali) in ambito ortopedico-riabilitativo.

### 1.2 Finalità
- **Finalità primaria:** raccolta centralizzata dei dati di valutazione funzionale dei pazienti per uso clinico (monitoraggio, follow-up, comunicazione con il medico prescrittore).
- **Finalità secondaria:** ricerca scientifica (studio di validazione del tapis roulant come strumento di misura della SSWS).

### 1.3 Dati trattati

| Categoria | Tipo dato | Classificazione GDPR |
|---|---|---|
| ID paziente pseudonimizzato | Codice alfanumerico (es. PAZ-20260319-A7F2) | Dato personale (pseudonimizzato) |
| Dati clinici | Velocità di cammino (SSWS), risultati test funzionali (TUG, Romberg, ecc.), livello dolore (VAS), farmaci | Dato sanitario (Art. 9) |
| Video | Registrazione del paziente che cammina su tapis roulant, con volto automaticamente oscurato (blur) | Dato sanitario; dato personale identificativo (anche con blur, il contesto clinico lo rende sanitario) |
| Metadati sessione | Data, ora, operatore, condizioni ambientali, calzature, ausili | Dato personale |

### 1.4 Soggetti interessati
- Pazienti adulti (40-80 anni) afferenti allo studio/ambulatorio per patologie ortopediche (artrosi, protesi anca/ginocchio)
- Stima numerosità: 50-200 pazienti/anno

### 1.5 Tecnologie utilizzate
- **Server:** Hetzner (datacenter UE — [CONFERMARE LOCALIZZAZIONE])
- **Software:** Applicazione web (Django/FastAPI) con database PostgreSQL
- **Storage file:** MinIO (S3-compatible, self-hosted)
- **Encryption:** TLS 1.3 in transito, LUKS/encryption at rest per i dischi
- **Video processing:** Blur automatico del volto tramite face detection (FFmpeg + modello ML) prima dell'upload
- **Condivisione:** Link con token crittografico + password + scadenza temporale

### 1.6 Flusso dei dati

```
Ambulatorio                          Server Hetzner (UE)
    │                                      │
    ├─ Raccolta dati (tablet/PC)           │
    ├─ Registrazione video                 │
    ├─ Face blur automatico (locale)       │
    ├─ Upload HTTPS ──────────────────────>├─ Storage cifrato
    │                                      ├─ Database PostgreSQL
    │                                      │
    │                                      ├─ Genera link protetto
    │                                      │      │
    │                                      │      ▼
    │                                 Paziente / Medico
    │                                 (accesso via browser,
    │                                  password + scadenza)
    │
    ├─ Tabella raccordo ID↔identità
    │  (conservata SEPARATAMENTE,
    │   offline o su sistema diverso)
```

---

## 2. Necessità e proporzionalità

### 2.1 Base giuridica
- **Per finalità clinica:** Art. 9(2)(h) GDPR — trattamento necessario per finalità di medicina preventiva, diagnosi, assistenza sanitaria. Supportato dal consenso esplicito del paziente (Art. 9(2)(a)).
- **Per finalità di ricerca:** Art. 9(2)(j) GDPR — trattamento necessario per finalità di ricerca scientifica, con garanzie adeguate (pseudonimizzazione). Richiede approvazione Comitato Etico.

### 2.2 Principio di minimizzazione
- **Pseudonimizzazione:** Sul server non sono presenti nome, cognome, codice fiscale, data di nascita. Solo ID pseudonimizzato.
- **Tabella di raccordo separata:** La corrispondenza ID ↔ identità reale è conservata su sistema separato (offline o diverso server), accessibile solo al titolare.
- **Blur volto:** I video vengono processati localmente per oscurare il volto PRIMA dell'upload. Sul server non arriva mai un video con volto riconoscibile.
- **Dati raccolti:** Solo quelli strettamente necessari alla valutazione clinica e alla ricerca.

### 2.3 Limitazione della conservazione
- **Dati clinici:** conservati per [DA DEFINIRE — proposta: durata del rapporto terapeutico + 10 anni, come da obblighi di legge per documentazione sanitaria]
- **Video:** conservati per [DA DEFINIRE — proposta: 2 anni dalla data di raccolta, poi cancellazione automatica, salvo diversa indicazione clinica]
- **Dati di ricerca (pseudonimizzati):** conservati per la durata dello studio + 5 anni post-pubblicazione (prassi standard)
- **Link di condivisione:** scadenza automatica dopo [DA DEFINIRE — proposta: 30 giorni]

### 2.4 Diritti degli interessati
Il paziente può esercitare in qualsiasi momento:
- **Accesso** (Art. 15): richiesta di copia dei propri dati
- **Rettifica** (Art. 16): correzione di dati inesatti
- **Cancellazione** (Art. 17): richiesta di eliminazione dei dati (compatibilmente con obblighi di legge)
- **Portabilità** (Art. 20): ricevere i propri dati in formato strutturato
- **Revoca del consenso** (Art. 7): in qualsiasi momento, senza pregiudizio
- **Reclamo** al Garante per la protezione dei dati personali

---

## 3. Valutazione dei rischi

### 3.1 Rischi identificati

| # | Rischio | Probabilità | Impatto | Livello | Mitigazione |
|---|---|---|---|---|---|
| R1 | Accesso non autorizzato al server | Media | Alto | **ALTO** | Firewall, SSH key-only, fail2ban, aggiornamenti auto |
| R2 | Data breach — esfiltrazione dati | Bassa | Molto alto | **ALTO** | Encryption at rest (LUKS), pseudonimizzazione, no dati identificativi sul server |
| R3 | Intercettazione dati in transito | Bassa | Alto | **MEDIO** | TLS 1.3 obbligatorio, HSTS |
| R4 | Accesso non autorizzato via link condivisione | Media | Medio | **MEDIO** | Password, scadenza, limite accessi, log, revoca |
| R5 | Perdita dati (guasto, ransomware) | Bassa | Alto | **MEDIO** | Backup cifrati incrementali su storage separata |
| R6 | Ricostruzione identità da video (nonostante blur) | Molto bassa | Alto | **BASSO** | Blur volto + pseudonimizzazione = doppio layer |
| R7 | Accesso alla tabella di raccordo | Bassa | Molto alto | **ALTO** | Conservazione offline/separata, accesso solo al titolare |
| R8 | Uso improprio dei dati da parte di terzi autorizzati | Bassa | Medio | **MEDIO** | Log accessi, scadenza link, informativa uso corretto |
| R9 | Mancata cancellazione a fine retention | Media | Medio | **MEDIO** | Procedura automatica di cancellazione schedulata |

### 3.2 Rischio residuo complessivo
Con le mitigazioni implementate: **MEDIO-BASSO**. Il principale rischio residuo è la compromissione del server, mitigata da encryption + pseudonimizzazione + assenza di dati direttamente identificativi.

---

## 4. Misure di sicurezza tecniche

### 4.1 Sicurezza del server
- [ ] Encryption at rest (LUKS per partizione dati)
- [ ] Firewall: solo porte 443 (HTTPS) e 22 (SSH)
- [ ] SSH: solo autenticazione con chiave, no password
- [ ] Fail2ban per protezione brute force
- [ ] Aggiornamenti di sicurezza automatici (unattended-upgrades)
- [ ] Monitoraggio uptime e integrità

### 4.2 Sicurezza applicativa
- [ ] Autenticazione operatore con password forte + 2FA
- [ ] Rate limiting sulle API
- [ ] Input validation e protezione OWASP Top 10
- [ ] Log di ogni accesso e operazione (audit trail)
- [ ] Session timeout dopo inattività

### 4.3 Sicurezza dei dati
- [ ] Pseudonimizzazione: ID paziente senza dati identificativi
- [ ] Tabella raccordo conservata separatamente (offline)
- [ ] Blur automatico volto prima dell'upload
- [ ] Backup cifrati (Restic + encryption) su Hetzner Storage Box separata
- [ ] Procedura di cancellazione a fine retention period

### 4.4 Sicurezza della condivisione
- [ ] Link con token crittografico (UUID v4 o simile)
- [ ] Password obbligatoria per accesso
- [ ] Scadenza temporale configurabile (default: 30 giorni)
- [ ] Numero massimo di accessi configurabile
- [ ] Log di ogni accesso (IP, timestamp, user-agent)
- [ ] Possibilità di revocare il link in qualsiasi momento
- [ ] Video in streaming (HLS), non scaricabile direttamente

---

## 5. Misure organizzative

- [ ] Consenso informato specifico per la piattaforma (documento separato)
- [ ] Informativa privacy (Art. 13) consegnata al paziente
- [ ] Formazione operatori sulla gestione dati sanitari
- [ ] Procedura di risposta a data breach (notifica al Garante entro 72h, Art. 33)
- [ ] Procedura per esercizio diritti degli interessati
- [ ] Revisione annuale della DPIA
- [ ] Registro dei trattamenti (Art. 30) — [DA CREARE]

---

## 6. Consultazione

### 6.1 Consulente privacy
- [ ] Sottoporre questa DPIA a consulente privacy/avvocato per validazione
- [ ] Confermare esenzione DPO
- [ ] Validare base giuridica

### 6.2 Comitato Etico
- [ ] Se i dati sono usati per ricerca: sottoporre protocollo al CE
- [ ] Includere nella documentazione CE il riferimento a questa DPIA

---

## 7. Approvazione

| Ruolo | Nome | Data | Firma |
|---|---|---|---|
| Titolare del trattamento | | | |
| Consulente privacy | | | |
| Responsabile IT | | | |

---

*Questo documento è una bozza da sottoporre a revisione professionale. Non costituisce consulenza legale.*
