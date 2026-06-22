/*
* Raccoglie le rotte per la gestione CRUD dell'entità articolo
* */
import { Router } from 'express';
import { articleRepository } from '../repository/articleRepository.js';
import { validate, validateId } from '../middleware/validate.js';
import {
  articleCreateSchema,
  articleUpdateSchema,
  articleFilterQuerySchema,
} from '../schemas/articleSchema.js';

const router = Router();

router.get('/', validate(articleFilterQuerySchema, 'query'), async (req, res, next) => {
  try {
    const { title, author, year, page, per_page } = req.query;
    return res.json(await articleRepository.findFiltered({
      title,
      author,
      year,
      page: page || 1,
      perPage: per_page || 10,
    }));
  } catch (err) { next(err); }
});

router.get('/:id', validateId, async (req, res, next) => {
  try {
    const article = await articleRepository.findById(req.params.id);
    if (!article) return res.status(404).json({ error: 'Not found' });
    res.json(article);
  } catch (err) {
    next(err);
  }
});

router.post('/', validate(articleCreateSchema), async (req, res, next) => {
  try {
    res.status(201).json(await articleRepository.create(req.body));
  } catch (err) {
    next(err);
  }
});

router.patch('/:id', validateId, validate(articleUpdateSchema), async (req, res, next) => {
  try {
    const article = await articleRepository.update(req.params.id, req.body);
    if (!article) return res.status(404).json({ error: 'Not found' });
    res.json(article);
  } catch (err) {
    next(err);
  }
});

router.delete('/:id', validateId, async (req, res, next) => {
  try {
    const deleted = await articleRepository.delete(req.params.id);
    if (!deleted) return res.status(404).json({ error: 'Not found' });
    res.status(204).end();
  } catch (err) {
    next(err);
  }
});

export default router;
