import { makeObservable, observable } from "mobx";

import type { Dictionary } from "@carefree0910/core";
import { ABCStore } from "@carefree0910/business";

import type { AvailablePlugins } from "@/schema/plugins";

export type IPluginsVisible = Partial<Record<AvailablePlugins, boolean>>;
class PluginsVisibleStore extends ABCStore<IPluginsVisible> {
  visible: IPluginsVisible = {};

  constructor() {
    super();
    makeObservable(this, {
      visible: observable,
    });
  }

  get info(): IPluginsVisible {
    return this.visible;
  }
}

const pluginsVisibleStore = new PluginsVisibleStore();
export const pluginIsVisible = (plugin: AvailablePlugins) =>
  pluginsVisibleStore.info[plugin] ?? true;
export const setPluginVisible = (plugin: AvailablePlugins, visible: boolean) =>
  pluginsVisibleStore.updateProperty(plugin, visible);

export type IPythonPluginsVisible = Dictionary<boolean>;
class PythonPluginsVisibleStore extends ABCStore<IPythonPluginsVisible> {
  visible: IPythonPluginsVisible = {};

  constructor() {
    super();
    makeObservable(this, {
      visible: observable,
    });
  }

  get info(): IPythonPluginsVisible {
    return this.visible;
  }
}

const pythonPluginsVisibleStore = new PythonPluginsVisibleStore();
export const pythonPluginIsVisible = (identifier: string) =>
  pythonPluginsVisibleStore.info[identifier] ?? true;
export const setPythonPluginVisible = (identifier: string, visible: boolean) =>
  pythonPluginsVisibleStore.updateProperty(identifier, visible);
