/*
* Classe per gestione entità Autore
* */
import db from '../db/client.js';

export class AuthorRepository {
  async findAll() {
    return db('authors').orderBy('surname').orderBy('name');
  }

  async findById(id) {
    return db('authors').where({ id }).first();
  }

  async create({ name, surname }) {
    const [id] = await db('authors').insert({ name, surname });
    return { id, name, surname };
  }

  async update(id, fields) {
    await db('authors').where({ id }).update(fields);
    return this.findById(id);
  }

  async delete(id) {
    const count = await db('authors').where({ id }).delete();
    return count > 0;
  }
}

export const authorRepository = new AuthorRepository();
