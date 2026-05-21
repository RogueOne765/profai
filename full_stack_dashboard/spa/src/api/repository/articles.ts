import type {Article, CreateArticleInput} from "../interfaces.ts";
import {client} from "../client.ts"

export class ArticleRepository {

  async getAll(): Promise<Article[]> {
    const response = await client.get('articles');
    return response.data;
  }
  async getById(id: number): Promise<Article> {
    const response = await client.get(`articles/${id}`);
    return response.data;
  }
  async getByAuthor(authorId: number): Promise<Article[]> {
    const response = await client.get('articles', { params: { author_id: authorId } });
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