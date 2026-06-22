import db from '../db/client.js';

export class ArticleRepository {
  withAuthors(qb) {
    return qb
      .leftJoin('article_authors', 'articles.id', 'article_authors.article_id')
      .leftJoin('authors', 'article_authors.author_id', 'authors.id')
      .select(
        'articles.*',
        'authors.id as author_id',
        'authors.name as author_name',
        'authors.surname as author_surname',
      );
  }

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

  async findAll() {
    const rows = await this.withAuthors(db('articles')).orderBy('articles.publication_date', 'desc');
    return this.groupArticles(rows);
  }

  async findFiltered({ title, author, year, page = 1, perPage = 10 }) {
    let query = this.withAuthors(db('articles'));

    if (title) {
      query = query.where('articles.title', 'like', `%${title}%`);
    }
    if (author) {
      query = query.whereRaw(
        "(authors.name || ' ' || authors.surname) LIKE ?",
        [`%${author}%`],
      );
    }
    if (year) {
      query = query.whereRaw(
        "CAST(strftime('%Y', articles.publication_date) AS INTEGER) = ?",
        [Number(year)],
      );
    }

    const [{ total }] = await query.clone()
      .clearSelect()
      .clearOrder()
      .countDistinct('articles.id as total');

    const rows = await query
      .orderBy('articles.publication_date', 'desc')
      .offset((page - 1) * perPage)
      .limit(perPage);

    return {
      data: this.groupArticles(rows),
      total,
      page,
      perPage,
      totalPages: Math.ceil(total / perPage),
    };
  }

  async findById(id, trx) {
    const client = trx ? trx : db;
    const rows = await this.withAuthors(client.table('articles')).where('articles.id', id);
    return this.groupArticles(rows)[0] ?? null;
  }

  async findByAuthor(authorId) {
    const rows = await this.withAuthors(db('articles'))
      .where('article_authors.author_id', authorId)
      .orderBy('articles.publication_date', 'desc');
    return this.groupArticles(rows);
  }

  async findByDoi(doi) {
    const rows = await this.withAuthors(db('articles')).where('articles.doi', doi);
    return this.groupArticles(rows)[0] ?? null;
  }

  async create({ title, abstract, publication_date, doi, author_ids = [] }) {
    return db.transaction(async (trx) => {
      const [id] = await trx('articles').insert({ title, abstract, publication_date, doi });
      if (author_ids.length) {
        await trx('article_authors').insert(
          author_ids.map((author_id) => ({ article_id: id, author_id })),
        );
      }
      return this.findById(id, trx);
    });
  }

  async update(id, { author_ids, ...fields }) {
    return db.transaction(async (trx) => {
      if (Object.keys(fields).length) {
        await trx('articles').where({ id }).update(fields);
      }
      if (author_ids !== undefined) {
        await trx('article_authors').where({ article_id: id }).delete();
        if (author_ids.length) {
          await trx('article_authors').insert(
            author_ids.map((author_id) => ({ article_id: id, author_id })),
          );
        }
      }
      return this.findById(id, trx);
    });
  }

  async delete(id) {
    const count = await db('articles').where({ id }).delete();
    return count > 0;
  }
}

export const articleRepository = new ArticleRepository();