import { RouterProvider } from 'react-router-dom'
import { MantineProvider } from '@mantine/core';
import { router } from './router'
import '@mantine/core/styles.css';
import {Notifications} from "@mantine/notifications";

export default function App() {
  return <>
    <MantineProvider defaultColorScheme="dark">
      <Notifications />
      <RouterProvider router={router} />
    </MantineProvider>
  </>
}
