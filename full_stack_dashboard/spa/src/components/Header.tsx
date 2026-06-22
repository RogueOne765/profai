import {ActionIcon} from "@mantine/core";
import { useDisclosure } from "@mantine/hooks";
import { ListIcon } from "@phosphor-icons/react";
import Drawer from "./Drawer";

export default function Header() {
  const [opened, { open, close }] = useDisclosure(false);

  return (
    <>
      <Drawer opened={opened} onClose={close} />

      <header className="py-4">
        <div className="flex gap-4 items-center">
          <ActionIcon
            size="lg"
            aria-label="Apri menu"
            onClick={open}
          >
            <ListIcon/>
          </ActionIcon>
          <span>Fullstack app</span>
        </div>
      </header>
    </>
  );
}
