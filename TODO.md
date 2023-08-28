* [ ] definire worker distinti per ogni tipologia di test (quindi immagine/container per categoria di tools implementata)
* [ ] eliminare redis e usare db come broker Celery
* [ ] modificare gestione frontend delle categorie (ora hard-coded per le cinque inizialmente implementate, ma serve dinamica in caso di nuove aggiunte)
* [ ] in caso di gestione dinamica categorie, è necessario inizializzare nel database le categorie dei tools implementati per usarle nel frontend
* [ ] aggiustare gestione Task in Frontend (con redis db): manca link da lista task a grafico (necessita un modo di collegare task a report, magari aggiungendo l'id del task al report nel db)
* [ ] per sviluppo locale del frontend, aggiustare i link dei fetch (funzionano solo usando docker non localmente)
* [ ] in caso di necessità, implementare autenticazione/autorizzazione API e login app frontend 
* [x] documentare i requisiti e gli step da implementare per creare un nuovo test
* [x] le url nei moduli react sono del tipo http://localhost vanno generalizzate per funzionare anche in ambienti di produzione 
* [x] splittare il README in più file: uno INSTALL per gli ops per l'installazione delle varie componenti e della soluzione,
      uno DEVELOPMENT per lo sviluppo
* [x] rimuovere, moduli, componenti, documentazione non utilizzata nel progetto
* [x] CI/CD su github actions
* [x] Perfomance - PageSpeed Insight PERFORMANCE
* [x] Security - ssllabsscan (test certificazione SSL)
* [x] Security - shcheck (check security headers)
* [x] SEO - PageSpeed Insight SEO 
* [x] SEO - robotparser
* [x] Accessibilità - Mauve++: docker non installa packages con npm (problema volume? path?)
* [x] Validazione - pa-website-validator: non installa source code e dipendenze (stesso problema mauve)
