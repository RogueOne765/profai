import { createBrowserRouter } from 'react-router-dom'
import BaseLayout from "./layouts/BaseLayout.tsx";

export const router = createBrowserRouter([
  {
    path: '/',
    Component: BaseLayout,
    children: [
      {
        index: true,
        lazy: async () => {
          return await import("./routes/home.tsx");
        },
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
