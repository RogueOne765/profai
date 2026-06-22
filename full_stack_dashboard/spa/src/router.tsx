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
        path: 'quotes/add',
        lazy: () => import('./routes/quotes-add'),
      },
      {
        path: '*',
        lazy: () => import('./routes/not-found'),
      },
    ],
  },
])
