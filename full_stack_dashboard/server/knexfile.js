/*
* File configurazione ORM Knex per interfaccia db SQlite
* */
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

export default {
  client: 'better-sqlite3',
  connection: {
    filename: process.env.DB_PATH || path.join(__dirname, '../data/app.db'),
  },
  useNullAsDefault: true,
  migrations: {
    directory: path.join(__dirname, 'db/migrations'),
    extension: 'js',
  },
};
