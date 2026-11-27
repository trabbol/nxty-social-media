# Greco Sgomberi: proposta di redesign del sito

Prototipo navigabile: `index.html`. Si apre in qualsiasi browser e le immagini sono in `img/`.
Tutti i contenuti vengono dal sito attuale (grecosgomberi.it): servizi, FAQ, storia, recensioni Google, contatti. Li ho riscritti e riorganizzati, senza copiarli pari pari.

## Cosa non funziona oggi

1. **Nessun percorso guidato.** La home elenca 5 servizi con frasi troncate ("…il noleggio di autoscale") e un lungo testo SEO. Chi arriva non capisce subito cosa fare.
2. **Il form è generico**: nome, email, telefono, servizio, messaggio. Non dà nulla in cambio e non aiuta a descrivere il lavoro.
3. **Contenuti rotti.** Nelle FAQ in home, "Quanto tempo richiede uno sgombero?" mostra ancora testo segnaposto in inglese (*"It is a long established fact…"*). Il form è in inglese ("Your Name", "Email Address").
4. **Dati incoerenti.** Si legge "dal 1980" ovunque, ma la pagina Azienda dice "Nel 1988 il fondatore Greco Giovanni…". Va chiarito con il cliente.
5. **Su mobile manca un contatto sempre visibile.** WhatsApp viene citato nelle pagine servizio ("invia le foto via WhatsApp"), ma non esiste un pulsante WhatsApp.
6. **Il punto di forza più bello è nascosto.** Il fondatore era restauratore di mobili antichi, e c'è il ritiro mobili con pagamento immediato. Sono due ottime ragioni per scegliere Greco, ma stanno in fondo a pagine secondarie.
7. Preloader "Loading", menu duplicato tre volte nel markup e template generico (Movingza) rendono la pagina lenta e poco riconoscibile.

## Cosa propone il nuovo design

| Area | Soluzione | Effetto sul funnel |
|---|---|---|
| Hero | Titolo orientato al beneficio, foto reale del camion, 4 riquadri "Cosa dobbiamo liberare?" | Il primo clic fa già partire il preventivo |
| Per chi | 6 situazioni (eredità, vendita casa, trasloco, ristrutturazione, attività, cantina) con testo e servizi su misura | L'utente si riconosce e resta sulla pagina |
| Servizi | Schede con "Cosa è incluso" apribile, senza cambiare pagina | Meno uscite, ogni scheda porta al preventivo |
| Vendi i tuoi mobili | Sezione dedicata: storia del restauratore e 3 passi fino al pagamento immediato, con pulsante WhatsApp per inviare le foto | Trasforma un costo in un guadagno: è la leva più forte |
| Preventivatore | 5 passi (servizio, dimensione, piano e ascensore, tempi ed extra, contatti). Consiglia l'autoscala se serve. Dà durata e mezzi indicativi e prepara il messaggio WhatsApp già compilato | Il cliente riceve subito qualcosa di utile. Lead qualificati, con tutti i dati per il sopralluogo |
| Fiducia | Badge Google "Eccellente", carosello delle recensioni reali, autorizzazione al trasporto rifiuti, "nessun costo nascosto" | Riduce l'ansia del "quanto mi costerà" |
| Zone | Verifica del comune con risposta immediata e mappa stilizzata dei comuni serviti | Rassicura chi è fuori Milano città |
| FAQ | Tutte le domande del sito, completate e ricercabili | Risponde alle obiezioni senza telefonata |
| Mobile | Barra fissa Chiama / WhatsApp / Preventivo, pulsante WhatsApp flottante su desktop | Il contatto è sempre a un tocco |
| Chiusura | Blocco "Ti richiamiamo noi" | Recupera chi non vuole compilare |

Identità visiva: dalla livrea dei mezzi riprendo il giallo e il nero, insieme al logo con il Duomo. Stile v2: impostazione industriale da scheda tecnica, con griglie a filo, angoli vivi e blocchi pieni giallo e nero. Font: Archivo Expanded per i titoli, Geist per il testo, Geist Mono per dati ed etichette.

## Da verificare con il cliente prima di andare live

- **Anno di fondazione**: 1980 o 1988?
- **Numero WhatsApp**: nel prototipo uso il 351 794 4522. Va confermato che sia attivo su WhatsApp.
- **Collegamento del preventivatore**: oggi invia il riepilogo su WhatsApp. In produzione va collegato anche a email o CRM (ad esempio Contact Form 7 o un webhook), con tracciamento delle conversioni (GA4 o Meta Pixel) su ogni passo.
- **Foto**: le immagini attuali sono foto di stock o generate. Foto reali di squadra, mezzi e un "prima e dopo" di cantine o appartamenti aumenterebbero molto la fiducia (slider prima/dopo come passo successivo).
- **Recensioni**: in pagina sono riportate con nome e iniziale del cognome. In produzione conviene mantenere il widget Google ufficiale o collegarle via API.
- **SEO**: mantenere le pagine servizio e le pagine dei comuni esistenti (Cormano, Cornaredo, Gorgonzola…), con lo stesso design, e aggiungere i dati strutturati `LocalBusiness` e `FAQPage`.
