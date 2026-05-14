import { Router } from 'express';
import { articleRepository } from '../repository/articleRepository.js';

const router = Router();

router.get('/', async (req, res, next) => {
  try {
    if (req.query.author_id) {
      return res.json(await articleRepository.findByAuthor(Number(req.query.author_id)));
    }
    res.json(await articleRepository.findAll());
  } catch (err) {
    next(err);
  }
});

router.get('/:id', async (req, res, next) => {
  try {
    const article = await articleRepository.findById(Number(req.params.id));
    if (!article) return res.status(404).json({ error: 'Not found' });
    res.json(article);
  } catch (err) {
    next(err);
  }
});

router.post('/', async (req, res, next) => {
  try {
    res.status(201).json(await articleRepository.create(req.body));
  } catch (err) {
    next(err);
  }
});

router.patch('/:id', async (req, res, next) => {
  try {
    const article = await articleRepository.update(Number(req.params.id), req.body);
    if (!article) return res.status(404).json({ error: 'Not found' });
    res.json(article);
  } catch (err) {
    next(err);
  }
});

router.delete('/:id', async (req, res, next) => {
  try {
    const deleted = await articleRepository.delete(Number(req.params.id));
    if (!deleted) return res.status(404).json({ error: 'Not found' });
    res.status(204).end();
  } catch (err) {
    next(err);
  }
});

export default router;