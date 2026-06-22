import { describe, it } from 'node:test';
import assert from 'node:assert/strict';
import { api } from './utils.js';

describe('/api/v1/authors', () => {
  let existingId;

  describe('POST /', () => {
    it('crea un autore con dati validi restituendo 201', async () => {
      const { status, body } = await api('POST', '/api/v1/authors', {
        name: 'Mario',
        surname: 'Rossi',
      });
      assert.equal(status, 201);
      assert.equal(body.name, 'Mario');
      assert.equal(body.surname, 'Rossi');
      assert.ok(body.id);
      existingId = body.id;
    });

    it('restituisce 400 quando i campi obbligatori mancano', async () => {
      const { status } = await api('POST', '/api/v1/authors', {});
      assert.equal(status, 400);
    });

    it('restituisce 400 quando nome o cognome sono vuoti', async () => {
      const { status } = await api('POST', '/api/v1/authors', {
        name: '',
        surname: '',
      });
      assert.equal(status, 400);
    });
  });

  describe('GET /', () => {
    it('restituisce tutti gli autori incluso quello appena creato', async () => {
      const { status, body } = await api('GET', '/api/v1/authors');
      assert.equal(status, 200);
      assert.ok(body.length >= 1);
      const found = body.find((a) => a.id === existingId);
      assert.ok(found);
      assert.equal(found.name, 'Mario');
    });
  });

  describe('GET /:id', () => {
    it('restituisce un autore esistente', async () => {
      const { status, body } = await api('GET', `/api/v1/authors/${existingId}`);
      assert.equal(status, 200);
      assert.equal(body.name, 'Mario');
      assert.equal(body.surname, 'Rossi');
    });

    it('restituisce 404 per un id inesistente', async () => {
      const { status } = await api('GET', '/api/v1/authors/99999');
      assert.equal(status, 404);
    });

    it('restituisce 400 per un id non valido', async () => {
      const { status } = await api('GET', '/api/v1/authors/abc');
      assert.equal(status, 400);
    });
  });

  describe('PATCH /:id', () => {
    it('aggiorna un autore esistente restituendo 200', async () => {
      const { status, body } = await api('PATCH', `/api/v1/authors/${existingId}`, {
        surname: 'Bianchi',
      });
      assert.equal(status, 200);
      assert.equal(body.surname, 'Bianchi');
      assert.equal(body.name, 'Mario');
    });

    it('restituisce 404 modificando un id inesistente', async () => {
      const { status } = await api('PATCH', '/api/v1/authors/99999', {
        name: 'X',
      });
      assert.equal(status, 404);
    });

    it('restituisce 400 quando il body è vuoto', async () => {
      const { status } = await api('PATCH', `/api/v1/authors/${existingId}`, {});
      assert.equal(status, 400);
    });
  });

  describe('DELETE /:id', () => {
    it('elimina un autore esistente restituendo 204', async () => {
      const { status, body } = await api('DELETE', `/api/v1/authors/${existingId}`);
      assert.equal(status, 204);
      assert.equal(body, null);
    });

    it('restituisce 404 eliminando un id inesistente', async () => {
      const { status } = await api('DELETE', '/api/v1/authors/99999');
      assert.equal(status, 404);
    });

    it('restituisce 404 richiedendo un autore eliminato', async () => {
      const { status } = await api('GET', `/api/v1/authors/${existingId}`);
      assert.equal(status, 404);
    });
  });
});
