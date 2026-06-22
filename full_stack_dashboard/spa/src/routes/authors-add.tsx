/*
* Rotta per creazione autore
* */
import { useState } from 'react';
import { TextInput, Button } from '@mantine/core';
import { useForm, isNotEmpty } from '@mantine/form';
import { notifications } from '@mantine/notifications';
import { authorRepo } from '../api/repository/authors';

interface AuthorForm {
  name: string;
  surname: string;
}

export function Component() {
  const [loading, setLoading] = useState(false);

  const form = useForm<AuthorForm>({
    initialValues: {
      name: '',
      surname: '',
    },
    validate: {
      name: isNotEmpty('Il nome e\' obbligatorio'),
      surname: isNotEmpty('Il cognome e\' obbligatorio'),
    },
  });

  const onSubmit = async (values: AuthorForm) => {
    setLoading(true);
    try {
      await authorRepo.create({
        name: values.name,
        surname: values.surname,
      });
      notifications.show({
        color: 'green',
        title: 'Successo',
        message: 'Autore creato con successo',
      });
      form.reset();
    } catch {
      notifications.show({
        color: 'red',
        title: 'Errore',
        message: "Impossibile creare l'autore",
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <section id="center" className="pb-10">
      <h1>Aggiungi autore</h1>
      <form className="flex justify-center w-full max-w-xl mx-auto" onSubmit={form.onSubmit(onSubmit)}>
        <div className="flex flex-col w-full gap-6">
          <TextInput
            className="text-left"
            label="Nome"
            placeholder="Inserisci il nome"
            {...form.getInputProps('name')}
          />

          <TextInput
            className="text-left"
            label="Cognome"
            placeholder="Inserisci il cognome"
            {...form.getInputProps('surname')}
          />

          <Button type="submit" loading={loading}>
            Salva
          </Button>
        </div>
      </form>
    </section>
  );
}
