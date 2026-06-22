import { describe, it } from 'node:test';
import assert from 'node:assert/strict';
import { api } from './utils.js';

describe('/api/v1/articles', () => {
  let authorId;
  let articleId;
  const createdAuthorIds = [];
  const extraArticleIds = [];

  describe('POST /', () => {
    it('crea un articolo con autore restituendo 201', async () => {
      const author = await api('POST', '/api/v1/authors', {
        name: 'Test',
        surname: 'Autore 1',
      });
      authorId = author.body.id;
      createdAuthorIds.push(authorId);

      const { status, body } = await api('POST', '/api/v1/articles', {
        title: 'Articolo di test',
        author_ids: [authorId],
      });
      assert.equal(status, 201);
      assert.equal(body.title, 'Articolo di test');
      assert.equal(body.authors.length, 1);
      assert.equal(body.authors[0].id, authorId);
      assert.ok(body.id);
      articleId = body.id;
    });

    it('crea un articolo con author_ids restituendo 201', async () => {
      const author = await api('POST', '/api/v1/authors', {
        name: 'Test',
        surname: 'Autore 2',
      });
      authorId = author.body.id;
      createdAuthorIds.push(authorId);

      const { status, body } = await api('POST', '/api/v1/articles', {
        title: 'Articolo con autore',
        author_ids: [authorId],
      });
      extraArticleIds.push(body.id);
      assert.equal(status, 201);
      assert.equal(body.title, 'Articolo con autore');
      assert.equal(body.authors.length, 1);
      assert.equal(body.authors[0].id, authorId);
    });

    it('restituisce 400 quando il titolo manca', async () => {
      const { status } = await api('POST', '/api/v1/articles', {});
      assert.equal(status, 400);
    });
  });

  describe('GET /', () => {
    it('restituisce risultati paginati', async () => {
      const { status, body } = await api('GET', '/api/v1/articles');
      assert.equal(status, 200);
      assert.ok(Array.isArray(body.data));
      assert.ok(body.total >= 2);
      assert.equal(body.page, 1);
      assert.equal(body.perPage, 10);
      assert.ok(body.totalPages >= 1);
    });

    it('supporta la paginazione', async () => {
      const a = await api('POST', '/api/v1/articles', { title: 'Pagina A', publication_date: '2024-01-01', author_ids: [authorId] });
      const b = await api('POST', '/api/v1/articles', { title: 'Pagina B', publication_date: '2024-02-01', author_ids: [authorId] });
      extraArticleIds.push(a.body.id, b.body.id);

      const { status, body } = await api('GET', '/api/v1/articles?per_page=2');
      assert.equal(status, 200);
      assert.equal(body.perPage, 2);
      assert.equal(body.data.length, 2);
      assert.ok(body.totalPages >= 1);
    });

    it('restituisce 400 per parametro pagina non valido', async () => {
      const { status } = await api('GET', '/api/v1/articles?page=-1');
      assert.equal(status, 400);
    });
  });

  describe('GET /:id', () => {
    it('restituisce un articolo esistente', async () => {
      const { status, body } = await api('GET', `/api/v1/articles/${articleId}`);
      assert.equal(status, 200);
      assert.equal(body.title, 'Articolo di test');
    });

    it('restituisce 404 per un id inesistente', async () => {
      const { status } = await api('GET', '/api/v1/articles/99999');
      assert.equal(status, 404);
    });
  });

  describe('PATCH /:id', () => {
    it('aggiorna il titolo di un articolo restituendo 200', async () => {
      const { status, body } = await api('PATCH', `/api/v1/articles/${articleId}`, {
        title: 'Titolo aggiornato',
      });
      assert.equal(status, 200);
      assert.equal(body.title, 'Titolo aggiornato');
    });

    it('aggiorna author_ids restituendo 200', async () => {
      const { status, body } = await api('PATCH', `/api/v1/articles/${articleId}`, {
        author_ids: [authorId],
      });
      assert.equal(status, 200);
      assert.equal(body.authors.length, 1);
      assert.equal(body.authors[0].id, authorId);
    });

    it('restituisce 404 modificando un id inesistente', async () => {
      const { status } = await api('PATCH', '/api/v1/articles/99999', {
        title: 'X',
      });
      assert.equal(status, 404);
    });
  });

  describe('DELETE /:id', () => {
    it('elimina un articolo esistente restituendo 204', async () => {
      const { status, body } = await api('DELETE', `/api/v1/articles/${articleId}`);
      assert.equal(status, 204);
    });

    it('restituisce 404 eliminando un id inesistente', async () => {
      const { status } = await api('DELETE', '/api/v1/articles/99999');
      assert.equal(status, 404);
    });

    it('pulisce gli articoli extra creati nei test', async () => {
      for (const id of extraArticleIds) {
        await api('DELETE', `/api/v1/articles/${id}`);
      }
    });

    it('pulisce gli autori creati nei test', async () => {
      for (const id of createdAuthorIds) {
        await api('DELETE', `/api/v1/authors/${id}`);
      }
    });
  });
});
