/*
* Classe per gestione citazioni verso il servizio BE
* */
import type {Quote, CreateQuoteInput} from "../interfaces.ts";
import {client} from "../client.ts"

export class QuoteRepository {
  basePath = 'quotes'

  async getById(id: number): Promise<Quote> {
    const response = await client.get(`${this.basePath}/${id}`);
    return response.data;
  }

  async getByArticle(articleId: number): Promise<Quote[]> {
    const response = await client.get(`${this.basePath}`, { params: { article_id: articleId } });
    return response.data;
  }

  async create(data: CreateQuoteInput): Promise<Quote> {
    const response = await client.post(`${this.basePath}`, data);
    return response.data;
  }

  async update(id: number, data: Partial<CreateQuoteInput>): Promise<Quote> {
    const response = await client.patch(`${this.basePath}/${id}`, data);
    return response.data;
  }

  async delete(id: number): Promise<void> {
    await client.delete(`${this.basePath}/${id}`);
  }
}

export const quoteRepo = new QuoteRepository()
