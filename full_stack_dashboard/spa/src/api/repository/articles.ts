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

  async getById(id: number): Promise<Article> {
    const response = await client.get(`articles/${id}`);
    return response.data;
  }
  async getByAuthor(authorId: number): Promise<Article[]> {
    const response = await client.get('articles', { params: { author_id: authorId } });
    return response.data;
  }
  async getFiltered(filters: ArticleFilters, page = 1, perPage = 10): Promise<PaginatedArticles> {
    const params: Record<string, string | number> = { page, per_page: perPage };
    if (filters.title) params.title = filters.title;
    if (filters.author) params.author = filters.author;
    if (filters.year) params.year = filters.year;
    const response = await client.get('articles', { params });
    return response.data;
  }
  async create(data: CreateArticleInput): Promise<Article> {
    const response = await client.post('articles', data);
    return response.data;
  }
  async update(id: number, data: Partial<CreateArticleInput>): Promise<Article> {
    const response = await client.patch(`articles/${id}`, data);
    return response.data;
  }
  async delete(id: number): Promise<void> {
    await client.delete(`articles/${id}`);
  }
}

export const articleRepo = new ArticleRepository()
