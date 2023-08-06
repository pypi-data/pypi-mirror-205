import { useMemo } from "react";
import { observer } from "mobx-react-lite";
import { Flex } from "@chakra-ui/react";

import { getRandomHash, identityMatrix2DFields } from "@carefree0910/core";
import { langStore, translate } from "@carefree0910/business";

import type { IPlugin } from "@/schema/plugins";
import { toastWord } from "@/utils/toast";
import { Add_Words } from "@/lang/add";
import { Toast_Words } from "@/lang/toast";
import { importMeta } from "@/actions/importMeta";
import { loadLocalProject, saveProject } from "@/actions/manageProjects";
import { getNewProject } from "@/stores/projects";
import CFButton from "@/components/CFButton";
import CFDivider from "@/components/CFDivider";
import CFHeading from "@/components/CFHeading";
import CFImageUploader from "@/components/CFImageUploader";
import { drawboardPluginFactory } from "../utils/factory";
import { floatingEvent } from "../components/Floating";
import Render from "../components/Render";
import { useClosePanel } from "../components/hooks";

const AddPlugin = ({ pluginInfo, ...props }: IPlugin) => {
  const id = useMemo(() => `add_${getRandomHash()}`, []);
  const lang = langStore.tgt;

  const closePanel = useClosePanel(id);
  const onNewProject = () => {
    toastWord("info", Toast_Words["adding-project-message"]);
    saveProject(
      async () =>
        loadLocalProject(
          { graphInfo: [], globalTransform: identityMatrix2DFields, ...getNewProject() },
          async () => {
            floatingEvent.emit({ type: "newProject", data: {} });
            toastWord("success", Toast_Words["add-project-success-message"]);
            closePanel();
          },
          true,
        ),
      true,
    );
  };

  return (
    <Render id={id} {...props}>
      <Flex w="100%" h="100%" direction="column">
        <CFHeading>{translate(Add_Words["add-plugin-header"], lang)}</CFHeading>
        <CFDivider />
        <CFButton w="100%" onClick={onNewProject}>
          {translate(Add_Words["new-project-button"], lang)}
        </CFButton>
        <CFImageUploader onUpload={closePanel}>
          <CFButton w="100%" mt="12px">
            {translate(Add_Words["upload-image-button"], lang)}
          </CFButton>
        </CFImageUploader>
        <CFButton
          w="100%"
          mt="12px"
          onClick={() => {
            importMeta({ lang, type: "add.text", metaData: {} });
            closePanel();
          }}>
          {translate(Add_Words["add-text-button"], lang)}
        </CFButton>
      </Flex>
    </Render>
  );
};

drawboardPluginFactory.register("add", true)(observer(AddPlugin));
