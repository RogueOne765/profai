/*
* Rotta per creazione articolo
* */
import { useEffect, useState } from 'react';
import { TextInput, Textarea, Button, MultiSelect } from '@mantine/core';
import {useForm, isNotEmpty} from '@mantine/form';
import { notifications } from '@mantine/notifications';
import { articleRepo } from '../api/repository/articles';
import { authorRepo } from '../api/repository/authors';
import type { Author } from '../api/interfaces';

interface ArticleForm {
  title: string;
  abstract: string;
  publication_date: string;
  doi: string;
  author_ids: number[];
}

export function Component() {
  const [authors, setAuthors] = useState<Author[]>([]);
  const [loading, setLoading] = useState(false);
  const [isBtnDisabled, setIsBtnDisabled] = useState(false);


  const form = useForm<ArticleForm>({
    initialValues: {
      title: '',
      abstract: '',
      publication_date: '',
      doi: '',
      author_ids: [],
    },
    validate: {
      title: isNotEmpty('Il titolo è obbligatorio'),
      abstract: isNotEmpty('L\'abstract è obbligatorio'),
      publication_date: isNotEmpty('La data di pubblicazione è obbligatoria'),
      author_ids: isNotEmpty('Seleziona almeno un autore'),
    },
  });

  useEffect(() => {
    authorRepo.getAll()
      .then((authors) => {
        if (authors?.length === 0) {
          setIsBtnDisabled(true)
          notifications.show({
            color: 'yellow',
            title: 'Attenzione',
            message: 'Nessun autore presente in archivio. Per creare un articolo, procedere prima con la creazione di almeno un autore.',
          })
        } else {
          setAuthors(authors)
        }
      })
      .catch(() => {
        setIsBtnDisabled(true)
        notifications.show({
          color: 'red',
          title: 'Errore',
          message: 'Impossibile caricare gli autori',
        })
      });
  }, []);

  const onSubmit = async (values: ArticleForm) => {
    setLoading(true);
    try {
      await articleRepo.create(values);
      notifications.show({
        color: 'green',
        title: 'Successo',
        message: 'Articolo creato con successo',
      });
      form.reset();
    } catch {
      notifications.show({
        color: 'red',
        title: 'Errore',
        message: 'Impossibile creare l\'articolo',
      });
    } finally {
      setLoading(false);
    }
  };

  const authorOptions = authors.map(author => ({
    value: author.id.toString(),
    label: `${author.name} ${author.surname}`,
  }));

  return (
    <section id="center" className="pb-10">
      <h1>Aggiungi articolo</h1>
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

          <Button type="submit" loading={loading} disabled={isBtnDisabled}>
            Salva
          </Button>
        </div>
      </form>
    </section>
  );
}
