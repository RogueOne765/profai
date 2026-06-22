/*
* Raccoglie le rotte per la gestione CRUD dell'entità autore
* */
import { Router } from 'express';
import { authorRepository } from '../repository/authorRepository.js';
import { validate, validateId } from '../middleware/validate.js';
import { authorCreateSchema, authorUpdateSchema } from '../schemas/authorSchema.js';

const router = Router();

/* Recupera tutti gli autori */
router.get('/', async (_req, res, next) => {
  try {
    res.json(await authorRepository.getAll());
  } catch (err) {
    next(err);
  }
});

/* Recupera un singolo autore per ID */
router.get('/:id', validateId, async (req, res, next) => {
  try {
    const author = await authorRepository.findById(req.params.id);
    if (!author) return res.status(404).json({ error: 'Not found' });
    res.json(author);
  } catch (err) {
    next(err);
  }
});

/* Crea un nuovo autore */
router.post('/', validate(authorCreateSchema), async (req, res, next) => {
  try {
    res.status(201).json(await authorRepository.create(req.body));
  } catch (err) {
    next(err);
  }
});

/* Aggiorna un autore esistente */
router.patch('/:id', validateId, validate(authorUpdateSchema), async (req, res, next) => {
  try {
    const author = await authorRepository.update(req.params.id, req.body);
    if (!author) return res.status(404).json({ error: 'Not found' });
    res.json(author);
  } catch (err) {
    next(err);
  }
});

/* Elimina un autore */
router.delete('/:id', validateId, async (req, res, next) => {
  try {
    const deleted = await authorRepository.delete(req.params.id);
    if (!deleted) return res.status(404).json({ error: 'Not found' });
    res.status(204).end();
  } catch (err) {
    next(err);
  }
});

export default router;
