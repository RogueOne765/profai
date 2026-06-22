import { useEffect, useState } from 'react';
import { TextInput, Button, Select } from '@mantine/core';
import {useForm, isNotEmpty} from '@mantine/form';
import { notifications } from '@mantine/notifications';
import { quoteRepo } from '../api/repository/quotes';
import { articleRepo } from '../api/repository/articles';
import type { Article } from '../api/interfaces';

interface QuoteForm {
  source: string;
  description: string;
  article_id: string;
}

export function Component() {
  const [articles, setArticles] = useState<Article[]>([]);
  const [loading, setLoading] = useState(false);

  const form = useForm<QuoteForm>({
    initialValues: {
      source: '',
      description: '',
      article_id: '',
    },
    validate: {
      source: isNotEmpty('La fonte è obbligatoria'),
      article_id: isNotEmpty("Seleziona un articolo"),
    },
  });

  useEffect(() => {
    articleRepo.getFiltered({})
      .then((paginatedArticles) => setArticles(paginatedArticles.data))
      .catch(() => notifications.show({
        color: 'red',
        title: 'Errore',
        message: 'Impossibile caricare gli articoli',
      }));
  }, []);

  const onSubmit = async (values: QuoteForm) => {
    setLoading(true);
    try {
      await quoteRepo.create({
        source: values.source,
        description: values.description || undefined,
        article_id: Number(values.article_id),
      });
      notifications.show({
        color: 'green',
        title: 'Successo',
        message: 'Citazione creata con successo',
      });
      form.reset();
    } catch {
      notifications.show({
        color: 'red',
        title: 'Errore',
        message: 'Impossibile creare la citazione',
      });
    } finally {
      setLoading(false);
    }
  };

  const articleOptions = articles.map(article => ({
    value: article.id.toString(),
    label: article.title,
  }));

  return (
    <section id="center" className="pb-10">
      <h1>Aggiungi citazione</h1>
      <form className="flex justify-center w-full max-w-xl mx-auto" onSubmit={form.onSubmit(onSubmit)}>
        <div className="flex flex-col w-full gap-6">
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

          <Select
            className="text-left"
            label="Articolo"
            placeholder="Seleziona un articolo"
            data={articleOptions}
            {...form.getInputProps('article_id')}
          />

          <Button type="submit" loading={loading}>
            Salva
          </Button>
        </div>
      </form>
    </section>
  );
}
