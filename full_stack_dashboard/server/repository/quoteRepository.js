/*
* Classe per gestione entità Citazione
* */
import db from '../db/client.js';

export class QuoteRepository {

  /* Inizializza il nome della tabella */
  constructor() {
    this.table = 'quotes'
  }

  /* Recupera tutte le citazioni in ordine decrescente di creazione */
  async getAll() {
    return db(this.table).orderBy('created_at', 'desc');
  }

  /* Recupera una singola citazione per ID */
  async findById(id) {
    return db(this.table).where({ id }).first() ?? null;
  }

  /* Crea una nuova citazione */
  async create({ source, description, article_id }) {
    const [id] = await db(this.table).insert({ source, description, article_id });
    return this.findById(id);
  }

  /* Aggiorna una citazione esistente */
  async update(id, fields) {
    await db(this.table).where({ id }).update(fields);
    return this.findById(id);
  }

  /* Elimina una citazione per ID */
  async delete(id) {
    const count = await db(this.table).where({ id }).delete();
    return count > 0;
  }
}

export const quoteRepository = new QuoteRepository();
