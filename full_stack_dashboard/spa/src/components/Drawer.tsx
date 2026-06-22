import { Drawer as MantineDrawer, NavLink } from "@mantine/core";
import { useNavigate } from "react-router-dom";

interface DrawerProps {
  opened: boolean;
  onClose: () => void;
}

export default function Drawer({ opened, onClose }: DrawerProps) {
  const navigate = useNavigate();

  function navigateTo(path: string) {
    navigate(path);
    onClose();
  }

  return (
    <MantineDrawer opened={opened} onClose={onClose} title="Menu">
      <NavLink label="Articoli" onClick={() => navigateTo("/articles")} />
      <NavLink label="Aggiungi articolo" onClick={() => navigateTo("/articles/add")} />
      <NavLink label="Aggiungi autore" onClick={() => navigateTo("/authors/add")} />
      <NavLink label="Aggiungi citazione" onClick={() => navigateTo("/quotes/add")} />
    </MantineDrawer>
  );
}
