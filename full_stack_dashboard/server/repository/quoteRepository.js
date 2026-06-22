/*
* Classe per gestione entità Citazione
* */
import db from '../db/client.js';

export class QuoteRepository {
  async findAll() {
    return db('quotes').orderBy('created_at', 'desc');
  }

  async findById(id) {
    return db('quotes').where({ id }).first() ?? null;
  }

  async findByArticle(articleId) {
    return db('quotes').where({ article_id: articleId }).orderBy('created_at', 'desc');
  }

  async create({ source, description, article_id }) {
    const [id] = await db('quotes').insert({ source, description, article_id });
    return this.findById(id);
  }

  async update(id, fields) {
    await db('quotes').where({ id }).update(fields);
    return this.findById(id);
  }

  async delete(id) {
    const count = await db('quotes').where({ id }).delete();
    return count > 0;
  }
}

export const quoteRepository = new QuoteRepository();
