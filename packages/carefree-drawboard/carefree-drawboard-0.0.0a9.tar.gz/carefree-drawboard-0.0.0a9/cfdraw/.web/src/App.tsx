import { Flex } from "@chakra-ui/react";
import { observer } from "mobx-react-lite";

import { useWebSocket } from "./stores/socket";
import { usePointerEvents } from "./stores/pointerEvents";
import { useUserInitialization } from "./stores/user";
import { useInitBoard } from "./hooks/useInitBoard";
import { useFileDropper } from "./hooks/useFileDropper";
import { useGridLines } from "./hooks/useGridLines";
import { usePreventDefaults } from "./hooks/usePreventDefaults";
import { useSyncPython } from "./hooks/usePython";
import BoardPanel from "./BoardPanel";

function App() {
  useWebSocket();
  useUserInitialization();
  useSyncPython();
  useInitBoard();
  useFileDropper();
  useGridLines();
  usePreventDefaults();
  usePointerEvents();

  return (
    <Flex h="100vh" className="p-editor" direction="column" userSelect="none">
      <Flex w="100%" flex={1}>
        <BoardPanel />
      </Flex>
    </Flex>
  );
}

export default observer(App);
