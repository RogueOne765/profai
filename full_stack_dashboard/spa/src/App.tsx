import { RouterProvider } from 'react-router-dom'
import { MantineProvider } from '@mantine/core';
import { router } from './router'
import '@mantine/core/styles.css';

export default function App() {
  return <>
    <MantineProvider defaultColorScheme="dark">
      <RouterProvider router={router} />
    </MantineProvider>
  </>
}
