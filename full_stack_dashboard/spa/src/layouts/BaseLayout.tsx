import { Outlet } from 'react-router-dom'
import Header from "../components/Header.tsx";

export default function BaseLayout() {
  return (
    <div className="custom-container min-h-screen">
      <Header/>
      <main>
        <Outlet/>
      </main>
    </div>
    )
}
