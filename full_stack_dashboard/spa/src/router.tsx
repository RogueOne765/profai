/*
* Le rotte seguono logica precisa per l'interazione con le entità disponibili:
* - /entity recupera lista elementi
* - /entity/add form creazione elemento
* - /entity/:id visualizzazione dettaglio elemento
* - /entity/edit/:id modifica elemento
* */
import {createBrowserRouter, redirect} from 'react-router-dom'
import BaseLayout from "./layouts/BaseLayout.tsx";

export const router = createBrowserRouter([
  {
    path: '/',
    Component: BaseLayout,
    children: [
      {
        index: true,
        loader: () => redirect('/articles'),
      },
      {
        path: 'articles',
        lazy: () => import('./routes/articles'),
      },
      {
        path: 'articles/add',
        lazy: () => import('./routes/articles-add'),
      },
      {
        path: 'articles/edit/:id',
        lazy: () => import('./routes/articles-edit'),
      },
      {
        path: 'articles/:id',
        lazy: () => import('./routes/articles-detail'),
      },
      {
        path: 'authors/add',
        lazy: () => import('./routes/authors-add'),
      },
      {
        path: 'quotes/add',
        lazy: () => import('./routes/quotes-add'),
      },
      {
        path: 'quotes/edit/:id',
        lazy: () => import('./routes/quotes-edit'),
      },
      {
        path: '*',
        lazy: () => import('./routes/not-found'),
      },
    ],
  },
])
