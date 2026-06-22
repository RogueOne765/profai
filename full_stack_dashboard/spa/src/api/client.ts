/*
* Espone come singleton il client di axios per gestione unificata chiamate a servizi esterni
* */
import axios from 'axios';

const baseUrl = import.meta.env.SERVER_API_URL || 'http://localhost:3000';
export const client = axios.create({ baseURL: baseUrl + '/api/v1' });
