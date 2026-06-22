/*
* Rotta di reindirizzamento per errori 404
* */
import { Link } from 'react-router-dom'

export function Component() {
  return (
    <section id="center">
      <h1>404 – Pagina non trovata</h1>
      <p>La pagina che cerchi non esiste.</p>
      <Link to="/">Torna alla home</Link>
    </section>
  )
}
