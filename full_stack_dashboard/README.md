# Full Stack Dashboard

## Struttura

```
full_stack_dashboard/
├── data/      # database SQLite
├── server/    # applicazione server-side
└── spa/       # single page application React
```

## Installazione

```bash
# Installazione dipendenze server
cd /server && npm install

# Eseguire script migrazione per db 
cd /server && npm run migrate

# Installazione dipendenze webapp e generazione bundle
cd /spa && npm install && npm run build
```

## Avvio

```bash
# server
cd server && npm start
```
Quindi visitare http://localhost:3000
