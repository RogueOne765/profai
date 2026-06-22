/*
* Classe per gestione autori verso il servizio BE
* */
import type {Author, CreateAuthorInput} from "../interfaces.ts";
import {client} from "../client.ts"

export class AuthorRepository {
  basePath = 'authors'

  async getAll(): Promise<Author[]> {
    const response = await client.get(`${this.basePath}`);
    return response.data;
  }

  async create(data: CreateAuthorInput): Promise<Author> {
    const response = await client.post(`${this.basePath}`, data);
    return response.data;
  }
}

export const authorRepo = new AuthorRepository()
