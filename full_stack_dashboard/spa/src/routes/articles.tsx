import { useEffect, useState, useMemo } from 'react';
import { NavLink, TextInput, Group, Pagination, Text, Select, Button } from '@mantine/core';
import { useNavigate } from 'react-router-dom';
import { articleRepo } from "../api/repository/articles.ts";
import { authorRepo } from "../api/repository/authors.ts";
import type { Article, Author } from "../api/interfaces.ts"

const currentYear = new Date().getFullYear();

export function Component() {
  const navigate = useNavigate();
  const [articles, setArticles] = useState<Article[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const [titleFilter, setTitleFilter] = useState('');
  const [authorFilter, setAuthorFilter] = useState<string | null>(null);
  const [yearFilter, setYearFilter] = useState('');
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [authors, setAuthors] = useState<Author[]>([]);

  const authorOptions = useMemo(() => authors.map((a) => ({
    value: `${a.name} ${a.surname}`,
    label: `${a.name} ${a.surname}`,
  })), [authors]);

  const yearError = useMemo(() => {
    if (!yearFilter) return null;
    const num = Number(yearFilter);
    if (!Number.isInteger(num) || num < 1900 || num > currentYear) {
      return `Year must be between 1900 and ${currentYear}`;
    }
    return null;
  }, [yearFilter]);

  const getFilters = (): Record<string, string> => {
    const filters: Record<string, string> = {};
    if (titleFilter) filters.title = titleFilter;
    if (authorFilter) filters.author = authorFilter;
    if (yearFilter && !yearError) filters.year = yearFilter;
    return filters;
  };

  const fetchArticles = (filters: Record<string, string>, pageNum: number) => {
    setLoading(true);
    articleRepo.getFiltered(filters, pageNum)
      .then((result) => {
        setArticles(result.data);
        setTotalPages(result.totalPages);
        setError(null);
      })
      .catch(() => setError('Failed to load articles'))
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    authorRepo.getAll().then(setAuthors).catch(() => {});
  }, []);

  useEffect(() => {
    fetchArticles(getFilters(), 1);
  }, []);

  const handleSearch = () => {
    setPage(1);
    fetchArticles(getFilters(), 1);
  };

  const handleReset = () => {
    setTitleFilter('');
    setAuthorFilter(null);
    setYearFilter('');
    setPage(1);
    fetchArticles({}, 1);
  };

  const handlePageChange = (p: number) => {
    setPage(p);
    fetchArticles(getFilters(), p);
  };

  if (error) return <section id="center"><p>{error}</p></section>;

  return (
    <section id="center">
      <h1>Articoli</h1>

      <div className="flex flex-col lg:flex-row">

        <div className="w-full lg:w-1/4">
          <Group className="mb-4 flex flex-col" align="flex-start">
            <TextInput
              className="w-full! text-left"
              placeholder="Cerca per titolo..."
              label="Titolo"
              value={titleFilter}
              onChange={(e) => setTitleFilter(e.currentTarget.value)}
            />
            <Select
              className="w-full! text-left"
              searchable
              clearable
              label="Autore"
              placeholder="Cerca per autore..."
              data={authorOptions}
              value={authorFilter}
              onChange={(v) => setAuthorFilter(v)}
            />
            <TextInput
              className="w-full! text-left"
              label="Anno"
              placeholder="Cerca per anno..."
              value={yearFilter}
              onChange={(e) => setYearFilter(e.currentTarget.value)}
              error={yearError}
            />
            <div className="flex flex-row gap-4 mt-4">
              <Button className="w-full!" onClick={handleSearch}>Cerca</Button>
              <Button className="w-full!" variant="outline" onClick={handleReset}>Reset</Button>
            </div>
          </Group>
        </div>


        <div className="w-full lg:w-3/4 lg:pl-6">
          {loading ? (
            <p>Loading...</p>
          ) : articles.length === 0 ? (
            <Text c="dimmed">No articles found</Text>
          ) : (
            <>
              {articles.map((article) => (
                <NavLink
                  key={article.id}
                  label={article.title}
                  description={article.authors.map(a => `${a.name} ${a.surname}`).join(', ')}
                  onClick={() => navigate(`/articles/${article.id}`)}
                />
              ))}
              {totalPages > 1 && (
                <Group className="mt-4" justify="center">
                  <Pagination total={totalPages} value={page} onChange={handlePageChange} />
                </Group>
              )}
            </>
          )}
        </div>

      </div>



    </section>
  );
}
