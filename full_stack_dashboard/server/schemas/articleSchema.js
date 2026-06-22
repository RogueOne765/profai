import { z } from 'zod';

export const articleCreateSchema = z.object({
  title: z.string().min(1, 'Title is required').max(500),
  abstract: z.string().nullable().optional(),
  publication_date: z.string().date().nullable().optional(),
  doi: z.string().nullable().optional(),
  author_ids: z.array(z.number().int().positive()).optional().default([]),
});

export const articleUpdateSchema = z.object({
  title: z.string().min(1).max(500).optional(),
  abstract: z.string().nullable().optional(),
  publication_date: z.string().date().nullable().optional(),
  doi: z.string().nullable().optional(),
  author_ids: z.array(z.number().int().positive()).optional(),
}).refine(data => Object.keys(data).length > 0, {
  message: 'At least one field must be provided',
});

export const articleFilterQuerySchema = z.object({
  title: z.string().optional(),
  author: z.string().optional(),
  year: z.string().optional(),
  page: z.preprocess(
    v => (v === undefined ? undefined : Number(v)),
    z.number().int().positive().optional(),
  ),
  per_page: z.preprocess(
    v => (v === undefined ? undefined : Number(v)),
    z.number().int().min(1).max(100).optional(),
  ),
});
