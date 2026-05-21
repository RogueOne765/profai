import { useEffect, useState } from 'react';
import {articleRepo} from "../api/repository/articles.ts";
import type {Article} from "../api/interfaces.ts"

export function Component() {
  const [articles, setArticles] = useState<Article[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    articleRepo.getAll()
      .then(setArticles)
      .catch(() => setError('Failed to load articles'))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <section id="center"><p>Loading...</p></section>;
  if (error) return <section id="center"><p>{error}</p></section>;

  return (
    <section id="center">
      <h1>Articoli</h1>
      { loading ? (<p>Loading...</p>) : ''}
      <ul>
        {articles.map((article) => (
          <li key={article.id}>
            <h2>{article.title}</h2>
            <p>{article.abstract}</p>
            <p>Authors: {article.authors.map(a => `${a.name} ${a.surname}`).join(', ')}</p>
          </li>
        ))}
      </ul>
    </section>
  );
}
