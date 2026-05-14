import { Router } from 'express';
import { authorRepository } from '../repository/authorRepository.js';

const router = Router();

router.get('/', async (_req, res, next) => {
  try {
    res.json(await authorRepository.findAll());
  } catch (err) {
    next(err);
  }
});

router.get('/:id', async (req, res, next) => {
  try {
    const author = await authorRepository.findById(Number(req.params.id));
    if (!author) return res.status(404).json({ error: 'Not found' });
    res.json(author);
  } catch (err) {
    next(err);
  }
});

router.post('/', async (req, res, next) => {
  try {
    res.status(201).json(await authorRepository.create(req.body));
  } catch (err) {
    next(err);
  }
});

router.patch('/:id', async (req, res, next) => {
  try {
    const author = await authorRepository.update(Number(req.params.id), req.body);
    if (!author) return res.status(404).json({ error: 'Not found' });
    res.json(author);
  } catch (err) {
    next(err);
  }
});

router.delete('/:id', async (req, res, next) => {
  try {
    const deleted = await authorRepository.delete(Number(req.params.id));
    if (!deleted) return res.status(404).json({ error: 'Not found' });
    res.status(204).end();
  } catch (err) {
    next(err);
  }
});

export default router;