export interface Author {
  id: number;
  name: string;
  surname: string;
}

export interface Article {
  id: number;
  title: string;
  abstract: string;
  publication_date: string;
  doi: string | null;
  authors: Author[];
}

export interface CreateArticleInput {
  title: string;
  abstract: string;
  publication_date: string;
  doi?: string;
  author_ids?: number[];
}

export interface Author {
  id: number;
  name: string;
  surname: string;
}
