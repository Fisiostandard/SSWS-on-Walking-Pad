
# SSWS self selected Walking speed  
La velocità a cui cammina una persona è un parametro di salute. 
Questo tipo di velocità del cammino spontaneo si chiama self-selected walking speed (SSWS). 
È un indicatore di salute dal punto di vista del vigore generale e soprattutto in ambito muscolo-scheletrico - ortopedico. 

## misurarla
È però una misura molto elusiva da misurare con precisione perché il soggetto può adattarsi in grande misura a quello che percepisce essere la richiesta funzionale dell'ambiente. In un certo senso sapendo di essere misurato, tende ad andare un po’ più spedito di come farebbe in piena solitudine e autonomia.
Misurare la velocità del cammino all'esterno è difficile perché è difficile trovare un percorso omogeneo sufficientemente lungo con condizioni ripetibili. Ci potrebbe essere una lieve salita o discesa. Potrebbero esserci buche. Potrebbero esserci altri passanti. Potrebbero esserci curve. Potrebbero esserci ostacoli. Potrebbero esserci brutto tempo. 
Quando si fa questa misura su un tapis roulant è importante che esista un meccanismo tale che la velocità del tapis roulant segua la volontà della persona. Vi sono apparecchi costosi che fanno questo. 

Credo che la letteratura sostenga l'uso del tapis roulant adattivo ("self-paced") rispetto al cammino overground




### Kingsmith WalkingPad
Nella mia pratica di medico ho acquistato due tapis roulant di marca Kingsmith, modello WalkingPad che hanno la capacità di accelerare in relazione a quanto il paziente spinge sul Tapis roulant. In pratica se il soggetto cammina sul davanti del tapis roulant, questo lo percepisce e accelera leggermente la velocità. Questa è una soluzione low cost che non offre un livello di qualità eccellente. Il software nativo tende ad accelerare molto rapidamente, rendendo tra l'altro anche leggermente pericolosa l'esecuzione del test. Però è possibile, a quanto pare, con Script in Python fatti con reverse engineering migliorare il software che muove il tapis roulant, rendendolo un po' più lento nell'accelerazione. 
Esistono già librerie pronte per interfacciarsi con il tappeto, ad esempio:
ph4-walkingpad (in Python)
node-noble-xiaomi-kingsmith-r1-pro-walkingpad (in Node.js)


Usando queste librerie, potremmo tenere il tappeto in modalità Manuale (M) e far controllare la velocità da un computer o da un piccolo Raspberry Pi via Bluetooth. Potremmo scrivere un algoritmo personalizzato che legge la posizione dei piedi del paziente (se il tappeto espone questo dato) o usa un sensore esterno (es. una telecamerina low-cost o un sensore di distanza).
Regola la velocità del tappeto inviando comandi Bluetooth continui, ma applicando una curva di accelerazione/decelerazione molto più dolce e controllata (es. variazioni massime di 0.1 km/h al secondo), ideale per chi ha protesi ad anca o ginocchio.

 Praticamente tutti gli studi clinici pubblicati finora utilizzano sistemi "instrumented" costosissimi (da decine di migliaia di euro, basati su pedane di forza integrate, come il GRAIL o i sistemi Motek). Non ci sono studi clinici validati peer-reviewed che utilizzino tapis roulant commerciali low-cost (come il Kingsmith) per la valutazione clinica ortopedica.
 Diciamo che questa potrebbe essere una nostra opportunità di contributo originale.





#### Consensus.app
https://consensus.app/ è un sito dove si può interrogare la letteratura scientifica con query in linguaggio comune
Io ho un abbonamento  di tipo "Consumer"  con la mie email <lorenzo.chiti@gmail.com>. La password viene inviata alla mia email volta volta (magic link)
Consensus offre delle API per sviluppatori (B2B), ma richiedono una registrazione a parte sul loro portale developer e hanno un costo basato sull'utilizzo
Sarebbe bello disporre di una chiave API (API Key) dedicata per far sì che un'applicazione esterna, uno script o un assistente IA come me possa interrogare direttamente Consensus aggirando l'invio del link  alla mia email. 




##### Obiettivo
Vorrei migliorare la gestione di questo sistema
Vorrei trovare evidenza in letteratura di usi di questo sistema
Idealmente in ambito di riabilitazione ortopedica dopo protesi di anca e ginocchio

Da un lato devo trovare legittimazione per usare questo setup, dall’altro vorrei renderlo disponibile ad un mio collega che sta facendo uno studio su protesi di rivestimento di Anca, cosiddette BHR, e le vuole confrontare con le protesi totali di Anca. Vorrebbe mostrare che c'è un miglioramento funzionale, misurandolo con la velocità spontanea del cammino ssws