/*
* Raccoglie principali interfacce per entità, form e servizi API utilizzate nell'app
* */

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

export interface CreateAuthorInput {
  name: string;
  surname: string;
}

export interface CreateArticleInput {
  title: string;
  abstract: string;
  publication_date: string;
  doi?: string;
  author_ids?: number[];
}

export interface Quote {
  id: number;
  source: string;
  description: string | null;
  article_id: number;
  created_at: string;
}

export interface CreateQuoteInput {
  source: string;
  description?: string;
  article_id: number;
}
