import { Router } from 'express';
import { articleRepository } from '../repository/articleRepository.js';

const router = Router();

router.get('/', async (req, res, next) => {
  try {
    const { title, author, author_id, year, page, per_page } = req.query;
    if (author_id && !title && !author && !year && !page && !per_page) {
      return res.json(await articleRepository.findByAuthor(Number(author_id)));
    }
    if (title || author || year || page || per_page) {
      return res.json(await articleRepository.findFiltered({
        title,
        author,
        year,
        page: page ? Number(page) : 1,
        perPage: per_page ? Number(per_page) : 10,
      }));
    }
    res.json(await articleRepository.findAll());
  } catch (err) { next(err); }
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