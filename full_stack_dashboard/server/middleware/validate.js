import { z } from 'zod';

/* Crea un middleware di validazione basato su schema Zod */
export function validate(schema, source = 'body') {
  return (req, res, next) => {
    const result = schema.safeParse(req[source]);
    if (!result.success) {
      return res.status(400).json({
        error: 'Validation error',
        details: result.error.issues.map(i => ({
          field: i.path.join('.'),
          message: i.message,
        })),
      });
    }
    req[source] = result.data;
    next();
  };
}

/* Schema per validazione ID numerico positivo */
const idSchema = z.object({
  id: z.coerce.number().int().positive('Invalid ID'),
});

/* Middleware preconfigurato per validare ID nei params */
export const validateId = validate(idSchema, 'params');
