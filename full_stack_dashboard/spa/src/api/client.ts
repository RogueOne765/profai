import axios from 'axios';

const baseUrl = import.meta.env.SERVER_API_URL || 'http://localhost:3000';
export const client = axios.create({ baseURL: baseUrl + '/api/v1' });
