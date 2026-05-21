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
const PORT = process.env.PORT || 3000;
const distPath = path.join(__dirname, '../spa/dist');

app.use(cors({ origin: process.env.SITE_URL || 'http://localhost:5173' }));
app.use(morgan('dev'));
app.use(express.json());

app.use('/api/v1/authors', authorsRouter);
app.use('/api/v1/articles', articlesRouter);
app.use('/api/v1/quotes', quotesRouter);


app.use(express.static(distPath));
app.get('*', (_req, res) => {
  res.sendFile(path.join(distPath, 'index.html'));
});

app.use((err, _req, res, _next) => {
  console.error(err);
  res.status(500).json({ error: 'Internal server error' });
});

app.listen(PORT, () => {
  console.log(`Server in ascolto su http://localhost:${PORT}`);
});
