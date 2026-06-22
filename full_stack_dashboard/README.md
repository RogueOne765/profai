# Full Stack Dashboard

## Installazione

```bash
# Installare dipendenze server
cd /server && npm install

# Eseguire script migrazione per db 
cd /server && npm run migrate

# Installare dipendenze webapp e generare bundle
cd /spa && npm install && npm run build
```

## Avvio

```bash
# avvio server (espone servizi e webapp)
cd /server && npm start
```
Quindi visitare http://localhost:3000


## Struttura

```
full_stack_dashboard/
├── data/                # destinazione file database SQLite
│
├── server/              
│   ├── index.js         # entry point — avvia il server
│   ├── app.js           # registra rotte, middeware e config server express
│   ├── knexfile.js      # configurazione ORM Knex (SQLite)
│   ├── db/              
│   │   ├── client.js    # client Knex inizializzato
│   │   └── migrations/  # script migrazione tabelle db
│   ├── middleware/      
│   │   └── validate.js  # validazione richieste via Zod
│   ├── repository/       # astrazione layer per interfaccia tabelle db
│   │   ├── articleRepository.js
│   │   ├── authorRepository.js
│   │   └── quoteRepository.js
│   ├── routes/           # definizione rotte API REST
│   │   ├── articles.js
│   │   ├── authors.js
│   │   └── quotes.js
│   ├── schemas/          # schemi validazione Zod
│   │   ├── articleSchema.js
│   │   ├── authorSchema.js
│   │   └── quoteSchema.js
│   └── tests/            # test con node:test
│       ├── articles.test.js
│       ├── authors.test.js
│       ├── quotes.test.js
│       └── utils.js
│
└── spa/                  # applicazione React + Mantine per UI
    ├── src/
    │   ├── main.tsx      # entry point React
    │   ├── App.tsx       # root component
    │   ├── router.tsx    # configurazione rotte
    │   ├── api/          # comunicazione con il server express
    │   │   ├── client.ts         # client Axios configurato
    │   │   ├── interfaces.ts     # interfacce per tipizzazione richieste/risposte API + oggetti interni
    │   │   └── repository/       # classi per astrazione interazione con backend divise per entità
    │   ├── components/   # componenti UI
    │   │   ├── Drawer.tsx
    │   │   ├── Header.tsx
    │   │   └── QuoteCard.tsx
    │   ├── layouts/      
    │   │   └── BaseLayout.tsx    # layout base per ogni pagina
    │   └── routes/       
    │       ├── articles.tsx         # lista articoli con filtri
    │       ├── articles-add.tsx     # creazione articolo
    │       ├── articles-detail.tsx  # dettaglio articolo
    │       ├── articles-edit.tsx    # modifica articolo
    │       ├── authors-add.tsx      # creazione autore
    │       ├── quotes-add.tsx       # creazione citazione
    │       ├── quotes-edit.tsx      # modifica citazione
    │       └── not-found.tsx        # pagina 404
    ├── public/           # asset statici
    └── dist/             # bundle di produzione
```
