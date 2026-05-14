import { Router } from 'express';
import { quoteRepository } from '../repository/quoteRepository.js';

const router = Router();

router.get('/', async (req, res, next) => {
  try {
    if (req.query.article_id) {
      return res.json(await quoteRepository.findByArticle(Number(req.query.article_id)));
    }
    res.json(await quoteRepository.findAll());
  } catch (err) {
    next(err);
  }
});

router.get('/:id', async (req, res, next) => {
  try {
    const quote = await quoteRepository.findById(Number(req.params.id));
    if (!quote) return res.status(404).json({ error: 'Not found' });
    res.json(quote);
  } catch (err) {
    next(err);
  }
});

router.post('/', async (req, res, next) => {
  try {
    res.status(201).json(await quoteRepository.create(req.body));
  } catch (err) {
    next(err);
  }
});

router.patch('/:id', async (req, res, next) => {
  try {
    const quote = await quoteRepository.update(Number(req.params.id), req.body);
    if (!quote) return res.status(404).json({ error: 'Not found' });
    res.json(quote);
  } catch (err) {
    next(err);
  }
});

router.delete('/:id', async (req, res, next) => {
  try {
    const deleted = await quoteRepository.delete(Number(req.params.id));
    if (!deleted) return res.status(404).json({ error: 'Not found' });
    res.status(204).end();
  } catch (err) {
    next(err);
  }
});

export default router;