import { Logger, shallowCopy } from "@carefree0910/core";
import { useSelecting } from "@carefree0910/business";

import type { AvailablePluginsAndPythonPlugins, IMakePlugin } from "@/schema/plugins";
import { pluginIsVisible, pythonPluginIsVisible } from "@/stores/pluginVisible";
import { drawboardPluginFactory } from "./utils/factory";
import { getNodeFilter } from "./utils/renderFilters";

// these lines are needed to make sure the plugins are registered
export * from "./_react/MetaPlugin";
export * from "./_react/SettingsPlugin";
export * from "./_react/ProjectPlugin";
export * from "./_react/AddPlugin";
export * from "./_react/ArrangePlugin";
export * from "./_react/UndoRedoPlugin";
export * from "./_react/DownloadPlugin";
export * from "./_react/DeletePlugin";
export * from "./_react/TextEditorPlugin";
export * from "./_react/GroupPlugin";
export * from "./_react/LinksPlugin";
export * from "./_react/BrushPlugin";
export * from "./_python/TextAreaPlugin";
export * from "./_python/QAPlugin";
export * from "./_python/FieldsPlugin";

export function makePlugin<T extends AvailablePluginsAndPythonPlugins>({
  key,
  type,
  containerRef,
  props: { renderInfo, pluginInfo, ...props },
}: IMakePlugin<T> & { key: string }) {
  renderInfo = shallowCopy(renderInfo);
  pluginInfo = shallowCopy(pluginInfo);
  if (renderInfo.follow && props.nodeConstraint === "none") {
    Logger.warn("cannot use `follow` with `targetNodeType` set to `none`");
    return null;
  }
  const Plugin = drawboardPluginFactory.get(type);
  if (!Plugin) {
    Logger.warn(`Plugin '${type}' not found`);
    return null;
  }
  const info = useSelecting("raw");
  if (!getNodeFilter(props.nodeConstraint)(info)) return null;
  const node = info.displayNode;
  const nodes = info.nodes;
  const updatedPluginInfo = { ...pluginInfo, node, nodes };
  if (!renderInfo.src)
    renderInfo.src =
      "https://user-images.githubusercontent.com/15677328/234536140-233d5f2d-b6fc-407b-b6df-59b5f37e0bcf.svg";
  if (drawboardPluginFactory.checkIsPython(type)) {
    renderInfo.isInvisible = !pythonPluginIsVisible((updatedPluginInfo as any).identifier);
  } else {
    renderInfo.isInvisible = !pluginIsVisible(type);
  }
  return (
    <Plugin
      key={key}
      renderInfo={renderInfo}
      pluginInfo={updatedPluginInfo}
      containerRef={containerRef}
      {...props}
    />
  );
}
