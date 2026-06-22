import type {Quote, CreateQuoteInput} from "../interfaces.ts";
import {client} from "../client.ts"

export class QuoteRepository {
  async getAll(): Promise<Quote[]> {
    const response = await client.get('quotes');
    return response.data;
  }
  async getById(id: number): Promise<Quote> {
    const response = await client.get(`quotes/${id}`);
    return response.data;
  }
  async getByArticle(articleId: number): Promise<Quote[]> {
    const response = await client.get('quotes', { params: { article_id: articleId } });
    return response.data;
  }
  async create(data: CreateQuoteInput): Promise<Quote> {
    const response = await client.post('quotes', data);
    return response.data;
  }
  async update(id: number, data: Partial<CreateQuoteInput>): Promise<Quote> {
    const response = await client.patch(`quotes/${id}`, data);
    return response.data;
  }
  async delete(id: number): Promise<void> {
    await client.delete(`quotes/${id}`);
  }
}

export const quoteRepo = new QuoteRepository()
