/*
* Classe per gestione entità Autore
* */
import db from '../db/client.js';

export class AuthorRepository {

  /* Inizializza il nome della tabella */
  constructor() {
    this.table = 'authors'
  }

  /* Recupera tutti gli autori ordinati per cognome e nome */
  async getAll() {
    return db(this.table).orderBy('surname').orderBy('name');
  }

  /* Recupera un singolo autore per ID */
  async findById(id) {
    return db(this.table).where({ id }).first();
  }

  /* Recupera autori multipli per lista ID */
  async findByIds(ids) {
    return db(this.table).whereIn('id', ids);
  }

  /* Cerca un autore per nome e cognome, escludendo opzionalmente un ID */
  async findByNameSurname(name, surname, excludeId) {
    let query = db(this.table).where({ name, surname });
    if (excludeId !== undefined) {
      query = query.whereNot({ id: excludeId });
    }
    return query.first();
  }

  /* Crea un nuovo autore */
  async create({ name, surname }) {
    const [id] = await db(this.table).insert({ name, surname });
    return { id, name, surname };
  }

  /* Aggiorna un autore esistente */
  async update(id, fields) {
    await db(this.table).where({ id }).update(fields);
    return this.findById(id);
  }

  /* Elimina un autore per ID */
  async delete(id) {
    const count = await db(this.table).where({ id }).delete();
    return count > 0;
  }
}

export const authorRepository = new AuthorRepository();
