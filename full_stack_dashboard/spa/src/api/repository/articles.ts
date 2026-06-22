/*
* Classe per gestione articoli verso il servizio BE
* */
import type {Article, CreateArticleInput} from "../interfaces.ts";
import {client} from "../client.ts"

export interface ArticleFilters {
  title?: string;
  author?: string;
  year?: string;
}

export interface PaginatedArticles {
  data: Article[];
  total: number;
  page: number;
  perPage: number;
  totalPages: number;
}

export class ArticleRepository {
  basePath = 'articles'

  async getById(id: number): Promise<Article> {
    const response = await client.get(`${this.basePath}/${id}`);
    return response.data;
  }

  async getList(filters: ArticleFilters, page = 1, perPage = 10): Promise<PaginatedArticles> {
    const params: Record<string, string | number> = { page, per_page: perPage };
    if (filters.title) params.title = filters.title;
    if (filters.author) params.author = filters.author;
    if (filters.year) params.year = filters.year;
    const response = await client.get(`${this.basePath}`, { params });
    return response.data;
  }

  async create(data: CreateArticleInput): Promise<Article> {
    const response = await client.post(`${this.basePath}`, data);
    return response.data;
  }

  async update(id: number, data: Partial<CreateArticleInput>): Promise<Article> {
    const response = await client.patch(`${this.basePath}/${id}`, data);
    return response.data;
  }

  async delete(id: number): Promise<void> {
    await client.delete(`${this.basePath}/${id}`);
  }
}

export const articleRepo = new ArticleRepository()
