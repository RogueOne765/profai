import { z } from 'zod';

/* Schema di validazione per creazione citazione */
export const quoteCreateSchema = z.object({
  source: z.string().min(1, 'Source is required').max(1000),
  description: z.string().optional(),
  article_id: z.number().int().positive().nullable().optional(),
});

/* Schema di validazione per aggiornamento citazione */
export const quoteUpdateSchema = z.object({
  source: z.string().min(1).max(1000).optional(),
  description: z.string().optional(),
  article_id: z.number().int().positive().nullable().optional(),
}).refine(data => Object.keys(data).length > 0, {
  message: 'At least one field must be provided',
});
