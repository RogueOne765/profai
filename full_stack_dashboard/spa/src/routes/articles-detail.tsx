/*
* Rotta per visualizzazione dettaglio articolo
* */
import { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Card, Text, Title, Group, Badge, Button } from '@mantine/core';
import { notifications } from '@mantine/notifications';
import { articleRepo } from '../api/repository/articles';
import { quoteRepo } from '../api/repository/quotes';
import QuoteCard from '../components/QuoteCard';
import type { Article, Quote } from '../api/interfaces';

export function Component() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [article, setArticle] = useState<Article | null>(null);
  const [quotes, setQuotes] = useState<Quote[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!id) return;
    Promise.all([
      articleRepo.getById(Number(id)),
      quoteRepo.getByArticle(Number(id)),
    ])
      .then(([articleData, quotesData]) => {
        setArticle(articleData);
        setQuotes(quotesData);
      })
      .catch(() => setError('Failed to load article'))
      .finally(() => setLoading(false));
  }, [id]);

  if (loading) return <section id="center"><p>Loading...</p></section>;
  if (error) return <section id="center"><p>{error}</p></section>;
  if (!article) return <section id="center"><p>Article not found</p></section>;

  const handleDelete = async () => {
    try {
      await articleRepo.delete(article.id);
      notifications.show({
        color: 'green',
        title: 'Successo',
        message: 'Articolo eliminato con successo',
      });
      navigate('/articles');
    } catch {
      notifications.show({
        color: 'red',
        title: 'Errore',
        message: 'Impossibile eliminare l\'articolo',
      });
    }
  };

  return (
    <section className="pb-10">

      <div className="flex justify-baseline">
        <Button variant="subtle" onClick={() => navigate('/articles')} className="">
          Back to articles
        </Button>
      </div>

      <div className="mt-10 flex flex-col lg:flex-row">

        <div className="w-full lg:w-3/4 lg:pr-6">
          <div className="text-left mb-20">
            <Title order={1} className="mb-4!">{article.title}</Title>
            <Text>{article.abstract}</Text>
          </div>

          <Group className="mt-10">
            <Button color="red" onClick={handleDelete}>Delete</Button>
            <Button onClick={() => navigate(`/articles/edit/${id}`)}>Edit</Button>
          </Group>
        </div>


        <div className="w-full lg:w-1/4">
          <Card className="shadow-sm p-6 rounded-md border mb-6 w-fit">
            <Group className="gap-1">
              <Text className="font-medium">Publication date:</Text>
              <Text>{new Date(article.publication_date).toLocaleDateString()}</Text>
            </Group>

            {article.doi && (
              <Group className="gap-1 mb-1">
                <Text className="font-medium">DOI:</Text>
                <Text>{article.doi}</Text>
              </Group>
            )}

            <Group className="gap-1">
              <Text className="font-medium">Authors:</Text>
              <Group className="gap-1">
                {article.authors.map((author) => (
                  <Badge key={author.id} variant="light" color="blue">
                    {author.name} {author.surname}
                  </Badge>
                ))}
              </Group>
            </Group>
          </Card>

          <div className="text-left">
            <Title order={2} className="mb-10">Quotes</Title>
            {quotes.length === 0 ? (
              <Text className="text-gray-500">No quotes for this article</Text>
            ) : (
              <div className="flex flex-col gap-4">
                {quotes.map((quote) => (
                  <QuoteCard key={quote.id} quote={quote} />
                ))}
              </div>
            )}
          </div>
        </div>

      </div>

    </section>
  );
}
