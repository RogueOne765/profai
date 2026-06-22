/*
* Raccoglie le rotte per la gestione CRUD dell'entità citazione
* */
import { Router } from 'express';
import { quoteRepository } from '../repository/quoteRepository.js';
import { validate, validateId } from '../middleware/validate.js';
import {
  quoteCreateSchema,
  quoteUpdateSchema,
} from '../schemas/quoteSchema.js';

const router = Router();

router.get('/', async (_req, res, next) => {
  try {
    res.json(await quoteRepository.findAll());
  } catch (err) {
    next(err);
  }
});

router.get('/:id', validateId, async (req, res, next) => {
  try {
    const quote = await quoteRepository.findById(req.params.id);
    if (!quote) return res.status(404).json({ error: 'Not found' });
    res.json(quote);
  } catch (err) {
    next(err);
  }
});

router.post('/', validate(quoteCreateSchema), async (req, res, next) => {
  try {
    res.status(201).json(await quoteRepository.create(req.body));
  } catch (err) {
    next(err);
  }
});

router.patch('/:id', validateId, validate(quoteUpdateSchema), async (req, res, next) => {
  try {
    const quote = await quoteRepository.update(req.params.id, req.body);
    if (!quote) return res.status(404).json({ error: 'Not found' });
    res.json(quote);
  } catch (err) {
    next(err);
  }
});

router.delete('/:id', validateId, async (req, res, next) => {
  try {
    const deleted = await quoteRepository.delete(req.params.id);
    if (!deleted) return res.status(404).json({ error: 'Not found' });
    res.status(204).end();
  } catch (err) {
    next(err);
  }
});

export default router;
