import express from 'express';
import path from 'path';
import { fileURLToPath } from 'url';
import cors from 'cors';
import morgan from 'morgan';
import authorsRouter from './routes/authors.js';
import articlesRouter from './routes/articles.js';
import quotesRouter from './routes/quotes.js';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const app = express();
const distPath = path.join(__dirname, '../spa/dist');

app.use(cors({ origin: process.env.SITE_URL || 'http://localhost:5173' }));
app.use(morgan(process.env.APP_ENV || 'dev'));
app.use(express.json());

/*
* Rotte che espongono servizi per recupero dati da DB
* */
app.use('/api/v1/authors', authorsRouter);
app.use('/api/v1/articles', articlesRouter);
app.use('/api/v1/quotes', quotesRouter);

/*
* Reindirizza tutte le altre richieste caricando asset del bundle compilato
* oppure index.html per la gestione delle rotte.
* */
app.use(express.static(distPath));
app.get('*', (_req, res) => {
  res.sendFile(path.join(distPath, 'index.html'));
});

/*
* Fallback per restituzione 500 in caso di eccezione non gestita
* */
app.use((err, _req, res, _next) => {
  console.error(err);
  res.status(500).json({ error: 'Internal server error' });
});

export default app;
