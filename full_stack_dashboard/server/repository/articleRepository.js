import db from '../db/client.js';

function groupArticles(rows) {
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

const WITH_AUTHORS = (qb) =>
  qb
    .leftJoin('article_authors', 'articles.id', 'article_authors.article_id')
    .leftJoin('authors', 'article_authors.author_id', 'authors.id')
    .select(
      'articles.*',
      'authors.id as author_id',
      'authors.name as author_name',
      'authors.surname as author_surname',
    );

export class ArticleRepository {
  async findAll() {
    const rows = await WITH_AUTHORS(db('articles')).orderBy('articles.publication_date', 'desc');
    return groupArticles(rows);
  }

  async findById(id) {
    const rows = await WITH_AUTHORS(db('articles')).where('articles.id', id);
    return groupArticles(rows)[0] ?? null;
  }

  async findByAuthor(authorId) {
    const rows = await WITH_AUTHORS(db('articles'))
      .where('article_authors.author_id', authorId)
      .orderBy('articles.publication_date', 'desc');
    return groupArticles(rows);
  }

  async findByDoi(doi) {
    const rows = await WITH_AUTHORS(db('articles')).where('articles.doi', doi);
    return groupArticles(rows)[0] ?? null;
  }

  async create({ title, abstract, publication_date, doi, author_ids = [] }) {
    return db.transaction(async (trx) => {
      const [id] = await trx('articles').insert({ title, abstract, publication_date, doi });
      if (author_ids.length) {
        await trx('article_authors').insert(
          author_ids.map((author_id) => ({ article_id: id, author_id })),
        );
      }
      return this.findById(id);
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
      return this.findById(id);
    });
  }

  async delete(id) {
    const count = await db('articles').where({ id }).delete();
    return count > 0;
  }
}

export const articleRepository = new ArticleRepository();