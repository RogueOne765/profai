/*
* Rotta per modifica informazioni articolo
* */
import { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {TextInput, Textarea, Button, MultiSelect, Card, Group, Title, Text} from '@mantine/core';
import { useForm, isNotEmpty } from '@mantine/form';
import { notifications } from '@mantine/notifications';
import { articleRepo } from '../api/repository/articles';
import { authorRepo } from '../api/repository/authors';
import { quoteRepo } from '../api/repository/quotes';
import type { Author, Quote } from '../api/interfaces';

interface ArticleForm {
  title: string;
  abstract: string;
  publication_date: string;
  doi: string;
  author_ids: number[];
}

export function Component() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [authors, setAuthors] = useState<Author[]>([]);
  const [quotes, setQuotes] = useState<Quote[]>([]);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);

  const form = useForm<ArticleForm>({
    initialValues: {
      title: '',
      abstract: '',
      publication_date: '',
      doi: '',
      author_ids: [],
    },
    validate: {
      title: isNotEmpty('Il titolo e\' obbligatorio'),
      abstract: isNotEmpty('L\'abstract e\' obbligatorio'),
      publication_date: isNotEmpty('La data di pubblicazione e\' obbligatoria'),
      author_ids: isNotEmpty('Seleziona almeno un autore'),
    },
  });

  useEffect(() => {
    if (!id) return;
    Promise.all([
      authorRepo.getAll(),
      articleRepo.getById(Number(id)),
      quoteRepo.getByArticle(Number(id)),
    ])
      .then(([authorsData, article, quotesData]) => {
        setAuthors(authorsData);
        setQuotes(quotesData);
        form.setValues({
          title: article.title,
          abstract: article.abstract,
          publication_date: article.publication_date.split('T')[0],
          doi: article.doi ?? '',
          author_ids: article.authors.map((a) => a.id),
        });
      })
      .catch(() => {
        notifications.show({
          color: 'red',
          title: 'Errore',
          message: 'Impossibile caricare l\'articolo',
        });
        navigate('/articles');
      })
      .finally(() => setLoading(false));
  }, [id]);

  const onSubmit = async (values: ArticleForm) => {
    setSubmitting(true);
    try {
      await articleRepo.update(Number(id), values);
      notifications.show({
        color: 'green',
        title: 'Successo',
        message: 'Articolo aggiornato con successo',
      });
      navigate(`/articles/${id}`);
    } catch {
      notifications.show({
        color: 'red',
        title: 'Errore',
        message: 'Impossibile aggiornare l\'articolo',
      });
    } finally {
      setSubmitting(false);
    }
  };

  const authorOptions = authors.map(author => ({
    value: author.id.toString(),
    label: `${author.name} ${author.surname}`,
  }));

  const handleQuoteDelete = async (qid: number) => {
    try {
      await quoteRepo.delete(qid);
      setQuotes((prev) => prev.filter((q) => q.id !== qid));
      notifications.show({
        color: 'green',
        title: 'Successo',
        message: 'Citazione eliminata con successo',
      });
    } catch {
      notifications.show({
        color: 'red',
        title: 'Errore',
        message: 'Impossibile eliminare la citazione',
      });
    }
  };

  if (loading) return <section><p>Loading...</p></section>;

  return (
    <section className="pb-10">
      <h1>Modifica articolo</h1>
      <form className="flex justify-center w-full max-w-xl mx-auto" onSubmit={form.onSubmit(onSubmit)}>
        <div className="flex flex-col w-full gap-6">
          <TextInput
            className="text-left"
            label="Titolo"
            placeholder="Inserisci il titolo"
            {...form.getInputProps('title')}
          />

          <Textarea
            className="text-left"
            label="Abstract"
            placeholder="Inserisci l'abstract"
            rows={4}
            {...form.getInputProps('abstract')}
          />

          <TextInput
            className="text-left"
            label="Data di pubblicazione"
            type="date"
            {...form.getInputProps('publication_date')}
          />

          <TextInput
            className="text-left"
            label="DOI"
            placeholder="Inserisci il DOI (opzionale)"
            {...form.getInputProps('doi')}
          />

          <MultiSelect
            className="text-left"
            label="Autori"
            placeholder="Seleziona gli autori"
            data={authorOptions}
            {...form.getInputProps('author_ids')}
            value={form.values.author_ids.map(String)}
            onChange={(values) => form.setFieldValue('author_ids', values.map(Number))}
          />

          <div className="flex gap-4">
            <Button type="submit" loading={submitting}>
              Salva
            </Button>
            <Button variant="outline" onClick={() => navigate(`/articles/${id}`)}>
              Annulla
            </Button>
          </div>
        </div>
      </form>

      <div className="mt-10">
        <Title order={2}>Citazioni</Title>
        {quotes.map((q) => (
          <Card key={q.id} className="mt-4 max-w-xl mx-auto text-left">
            <Title order={4}>{q.source}</Title>
            <Text>{q.description}</Text>
            <Group className="mt-2">
              <Button size="compact-xs" onClick={() => navigate(`/quotes/edit/${q.id}`)}>
                Modifica
              </Button>
              <Button size="compact-xs" color="red" onClick={() => handleQuoteDelete(q.id)}>
                Elimina
              </Button>
            </Group>
          </Card>
        ))}
      </div>

    </section>
  );
}
