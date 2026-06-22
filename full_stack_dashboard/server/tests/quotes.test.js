import { describe, it } from 'node:test';
import assert from 'node:assert/strict';
import { api } from './utils.js';

describe('/api/v1/quotes', () => {
  let quoteId;
  let prerequisiteAuthorId;
  let prerequisiteArticleId;
  let extraQuoteId;

  describe('POST /', () => {
    it('crea una citazione con article_id restituendo 201', async () => {
      const author = await api('POST', '/api/v1/authors', { name: 'Test', surname: 'Author' });
      const article = await api('POST', '/api/v1/articles', { title: 'Articolo target', author_ids: [author.body.id] });
      prerequisiteAuthorId = author.body.id;
      prerequisiteArticleId = article.body.id;

      const { status, body } = await api('POST', '/api/v1/quotes', {
        source: 'Una citazione notevole',
        description: 'Descrizione della citazione',
        article_id: article.body.id,
      });
      assert.equal(status, 201);
      assert.equal(body.source, 'Una citazione notevole');
      assert.equal(body.description, 'Descrizione della citazione');
      assert.equal(body.article_id, article.body.id);
      assert.ok(body.id);
      quoteId = body.id;
    });

    it('crea una citazione senza article_id restituendo 201', async () => {
      const { status, body } = await api('POST', '/api/v1/quotes', {
        source: 'Una citazione isolata',
      });
      assert.equal(status, 201);
      assert.equal(body.source, 'Una citazione isolata');
      assert.equal(body.article_id, null);
      extraQuoteId = body.id;
    });

    it('restituisce 400 quando la fonte manca', async () => {
      const { status } = await api('POST', '/api/v1/quotes', {});
      assert.equal(status, 400);
    });
  });

  describe('GET /', () => {
    it('restituisce tutte le citazioni', async () => {
      const { status, body } = await api('GET', '/api/v1/quotes');
      assert.equal(status, 200);
      assert.ok(body.length >= 2);
    });
  });

  describe('GET /:id', () => {
    it('restituisce una citazione esistente', async () => {
      const { status, body } = await api('GET', `/api/v1/quotes/${quoteId}`);
      assert.equal(status, 200);
      assert.equal(body.source, 'Una citazione notevole');
    });

    it('restituisce 404 per un id inesistente', async () => {
      const { status } = await api('GET', '/api/v1/quotes/99999');
      assert.equal(status, 404);
    });
  });

  describe('PATCH /:id', () => {
    it('aggiorna una citazione esistente restituendo 200', async () => {
      const { status, body } = await api('PATCH', `/api/v1/quotes/${quoteId}`, {
        description: 'Descrizione aggiornata',
      });
      assert.equal(status, 200);
      assert.equal(body.description, 'Descrizione aggiornata');
    });

    it('restituisce 400 quando il body è vuoto', async () => {
      const { status } = await api('PATCH', `/api/v1/quotes/${quoteId}`, {});
      assert.equal(status, 400);
    });
  });

  describe('DELETE /:id', () => {
    it('elimina una citazione esistente restituendo 204', async () => {
      const { status, body } = await api('DELETE', `/api/v1/quotes/${quoteId}`);
      assert.equal(status, 204);
      assert.equal(body, null);
    });

    it('restituisce 404 eliminando un id inesistente', async () => {
      const { status } = await api('DELETE', '/api/v1/quotes/99999');
      assert.equal(status, 404);
    });

    it('pulisce la citazione senza article_id', async () => {
      await api('DELETE', `/api/v1/quotes/${extraQuoteId}`);
    });

    it('pulisce articolo e autore prerequisiti', async () => {
      await api('DELETE', `/api/v1/articles/${prerequisiteArticleId}`);
      await api('DELETE', `/api/v1/authors/${prerequisiteAuthorId}`);
    });
  });
});
