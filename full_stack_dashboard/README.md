# Full Stack Dashboard

## Struttura

```
full_stack_dashboard/
├── data/      # destinazione database SQLite
├── server/    # applicazione server-side
└── spa/       # spa React
```

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
