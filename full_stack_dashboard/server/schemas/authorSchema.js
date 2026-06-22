import { z } from 'zod';

export const authorCreateSchema = z.object({
  name: z.string().min(1, 'Name is required').max(200),
  surname: z.string().min(1, 'Surname is required').max(200),
});

export const authorUpdateSchema = z.object({
  name: z.string().min(1).max(200).optional(),
  surname: z.string().min(1).max(200).optional(),
}).refine(data => Object.keys(data).length > 0, {
  message: 'At least one field must be provided',
});
