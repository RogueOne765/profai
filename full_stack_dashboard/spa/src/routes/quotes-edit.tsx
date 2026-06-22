import { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { TextInput, Button, Select } from '@mantine/core';
import { useForm, isNotEmpty } from '@mantine/form';
import { notifications } from '@mantine/notifications';
import { quoteRepo } from '../api/repository/quotes';
import { articleRepo } from '../api/repository/articles';

interface QuoteForm {
  source: string;
  description: string;
}

export function Component() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [articleTitle, setArticleTitle] = useState('');
  const [articleId, setArticleId] = useState<number | null>(null);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);

  const form = useForm<QuoteForm>({
    initialValues: {
      source: '',
      description: '',
    },
    validate: {
      source: isNotEmpty('La fonte e\' obbligatoria'),
    },
  });

  useEffect(() => {
    if (!id) return;
    quoteRepo.getById(Number(id))
      .then(async (quote) => {
        setArticleId(quote.article_id);
        const article = await articleRepo.getById(quote.article_id);
        setArticleTitle(article.title);
        form.setValues({
          source: quote.source,
          description: quote.description ?? '',
        });
      })
      .catch(() => {
        notifications.show({
          color: 'red',
          title: 'Errore',
          message: 'Impossibile caricare la citazione',
        });
        navigate('/articles');
      })
      .finally(() => setLoading(false));
  }, [id]);

  const onSubmit = async (values: QuoteForm) => {
    setSubmitting(true);
    try {
      await quoteRepo.update(Number(id), {
        source: values.source,
        description: values.description || undefined,
        article_id: articleId!,
      });
      notifications.show({
        color: 'green',
        title: 'Successo',
        message: 'Citazione aggiornata con successo',
      });
      navigate(`/articles/edit/${articleId}`);
    } catch {
      notifications.show({
        color: 'red',
        title: 'Errore',
        message: 'Impossibile aggiornare la citazione',
      });
    } finally {
      setSubmitting(false);
    }
  };

  if (loading) return <section id="center"><p>Loading...</p></section>;

  return (
    <section id="center" className="pb-10">
      <h1>Modifica citazione</h1>
      <form className="flex justify-center w-full max-w-xl mx-auto" onSubmit={form.onSubmit(onSubmit)}>
        <div className="flex flex-col w-full gap-6">
          <Select
            className="text-left"
            label="Articolo"
            data={[{ value: String(articleId), label: articleTitle }]}
            value={String(articleId)}
            disabled
          />

          <TextInput
            className="text-left"
            label="Fonte"
            placeholder="Inserisci la fonte"
            {...form.getInputProps('source')}
          />

          <TextInput
            className="text-left"
            label="Descrizione"
            placeholder="Inserisci la descrizione (opzionale)"
            {...form.getInputProps('description')}
          />

          <div className="flex gap-4">
            <Button type="submit" loading={submitting}>
              Salva
            </Button>
            <Button variant="outline" onClick={() => navigate(`/articles/edit/${articleId}`)}>
              Annulla
            </Button>
          </div>
        </div>
      </form>
    </section>
  );
}
