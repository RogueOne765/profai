/*
* Espone come singleton il client di knex (ORM) per SQLite da utilizzare all'interno dell'applicazione
* */
import knex from 'knex';
import knexConfig from '../knexfile.js';

const db = knex(knexConfig);

export default db;
