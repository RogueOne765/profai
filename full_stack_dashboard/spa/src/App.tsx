/*
* Wrapper principale dell'app, contiene:
* - provider del framework Mantine (per UI)
* - componente per visualizzazione notifiche (a livello globale nell'app)
* - componente per proiezione contenuto rotte
* */
import { RouterProvider } from 'react-router-dom'
import { MantineProvider } from '@mantine/core';
import { router } from './router'
import '@mantine/core/styles.css';
import '@mantine/notifications/styles.css';
import {Notifications} from "@mantine/notifications";

export default function App() {
  return <>
    <MantineProvider defaultColorScheme="dark">
      <Notifications />
      <RouterProvider router={router} />
    </MantineProvider>
  </>
}
