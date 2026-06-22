/*
* Classe per gestione entità Articolo
* */
import db from '../db/client.js';

export class ArticleRepository {
  /* Inizializza i nomi delle tabelle */
  constructor() {
    this.authorsTable = 'authors'
    this.articlesTable = 'articles'
    this.articlesAutorsTable = 'article_authors'
  }


  /*
  * Data una lista di articoli, esegue join delle tabelle article_authors e authors per incrociare dati articolo e dati autori corrispondenti.
  * Accetta come argomento query builder di knex.
  * */
  joinAuthors(qb) {
    return qb
      .leftJoin(this.articlesAutorsTable, 'articles.id', 'article_authors.article_id')
      .leftJoin(this.authorsTable, 'article_authors.author_id', 'authors.id')
      .select(
        'articles.*',
        'authors.id as author_id',
        'authors.name as author_name',
        'authors.surname as author_surname',
      );
  }

  /*
  * Crea oggetto da esporre tramite API che combina articoli e dati autori.
  * Esempio struttura:
  * [
  *   ...articoli,
  *   {
  *     ...dati articolo,
  *     authors: [
  *       ...lista autori collegati ad articolo,
  *       {
  *         id: ...,
  *         name: ...,
  *         surname: ...
  *       }
  *     ]
  *   }
  * ]
  * */
  groupArticles(rows) {
    const map = new Map();
    for (const row of rows) {
      if (!map.has(row.id)) {
        const { author_id, author_name, author_surname, ...article } = row;
        map.set(row.id, { ...article, authors: [] });
      }
      if (row.author_id) {
        map.get(row.id).authors.push({
          id: row.author_id,
          name: row.author_name,
          surname: row.author_surname,
        });
      }
    }
    return [...map.values()];
  }

  /* Recupera articoli con filtri, paginazione e autori associati */
  async findFiltered({ title, author, year, page = 1, perPage = 10 }) {
    let baseQuery = db(this.articlesTable);

    if (title) {
      baseQuery = baseQuery.where('articles.title', 'like', `%${title}%`);
    }
    if (author) {
      baseQuery = baseQuery
        .join('article_authors', 'articles.id', 'article_authors.article_id')
        .join('authors', 'article_authors.author_id', 'authors.id')
        .whereRaw(
          "(authors.name || ' ' || authors.surname) LIKE ?",
          [`%${author}%`],
        );
    }
    if (year) {
      baseQuery = baseQuery.whereRaw(
        "CAST(strftime('%Y', articles.publication_date) AS INTEGER) = ?",
        [Number(year)],
      );
    }

    const [{ total }] = await baseQuery.clone()
      .clearSelect()
      .clearOrder()
      .countDistinct('articles.id as total');

    const ids = (await baseQuery.clone()
      .clearSelect()
      .select('articles.id', 'articles.publication_date')
      .distinct()
      .orderBy('articles.publication_date', 'desc')
      .offset((page - 1) * perPage)
      .limit(perPage))
      .map(r => r.id);

    const rows = ids.length
      ? await this.joinAuthors(db(this.articlesTable))
          .whereIn('articles.id', ids)
          .orderBy('articles.publication_date', 'desc')
      : [];

    return {
      data: this.groupArticles(rows),
      total,
      page,
      perPage,
      totalPages: Math.ceil(total / perPage),
    };
  }

  /* Recupera un singolo articolo per ID con autori associati */
  async findById(id, trx) {
    const client = trx ? trx : db;
    const rows = await this.joinAuthors(client.table(this.articlesTable)).where('articles.id', id);
    return this.groupArticles(rows)[0] ?? null;
  }

  /* Crea un nuovo articolo con eventuali autori associati */
  async create({ title, abstract, publication_date, doi, author_ids = [] }) {
    return db.transaction(async (trx) => {
      const [id] = await trx(this.articlesTable).insert({ title, abstract, publication_date, doi });
      if (author_ids.length) {
        await trx('article_authors').insert(
          author_ids.map((author_id) => ({ article_id: id, author_id })),
        );
      }
      return this.findById(id, trx);
    });
  }

  /* Aggiorna un articolo e i suoi autori associati */
  async update(id, { author_ids, ...fields }) {
    return db.transaction(async (trx) => {
      const exists = await trx(this.articlesTable).where({ id }).first();
      if (!exists) return null;

      if (Object.keys(fields).length) {
        await trx(this.articlesTable).where({ id }).update(fields);
      }
      if (author_ids !== undefined) {
        await trx(this.articlesAutorsTable).where({ article_id: id }).delete();
        if (author_ids.length) {
          await trx(this.articlesAutorsTable).insert(
            author_ids.map((author_id) => ({ article_id: id, author_id })),
          );
        }
      }
      return this.findById(id, trx);
    });
  }

  /* Elimina un articolo per ID */
  async delete(id) {
    const count = await db(this.articlesTable).where({ id }).delete();
    return count > 0;
  }
}

export const articleRepository = new ArticleRepository();
