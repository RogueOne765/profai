import type {Author} from "../interfaces.ts";
import {client} from "../client.ts"

export class AuthorRepository {

  async getAll(): Promise<Author[]> {
    const response = await client.get('authors');
    return response.data;
  }
  async getById(id: number): Promise<Author> {
    const response = await client.get(`authors/${id}`);
    return response.data;
  }
}

export const authorRepo = new AuthorRepository()