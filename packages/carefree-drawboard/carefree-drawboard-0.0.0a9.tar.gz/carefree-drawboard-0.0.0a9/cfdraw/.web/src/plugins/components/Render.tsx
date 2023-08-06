import type { ChakraComponent } from "@chakra-ui/react";
import { useLayoutEffect, useMemo } from "react";
import { observer } from "mobx-react-lite";

import { Coordinate, getRandomHash, INodes, PivotType, shallowCopy } from "@carefree0910/core";
import {
  boardBBoxToDom,
  injectNodeTransformEventCallback,
  removeNodeTransformEventCallback,
  useBoardContainerLeftTop,
  useBoardContainerWH,
  useIsReady,
  useSelectHooks,
  useSelecting,
} from "@carefree0910/business";

import type { IRender } from "@/schema/plugins";
import { DEFAULT_PLUGIN_SETTINGS } from "@/utils/constants";
import { getNodeFilter } from "../utils/renderFilters";
import Floating, {
  floatingRenderEvent,
  getExpandId,
  getExpandPosition,
  IFloatingRenderEvent,
} from "./Floating";

let DEBUG_PREFIX: string | undefined;

const Render = (({ id, nodeConstraint, renderInfo, containerRef, children, ...props }: IRender) => {
  const _id = useMemo(() => id ?? `plugin_${getRandomHash()}`, [id]);
  let { w, h, iconW, iconH, pivot, follow, offsetX, offsetY, expandOffsetX, expandOffsetY } =
    renderInfo;
  iconW ??= DEFAULT_PLUGIN_SETTINGS.iconW;
  iconH ??= DEFAULT_PLUGIN_SETTINGS.iconH;
  pivot ??= DEFAULT_PLUGIN_SETTINGS.pivot as PivotType;
  follow ??= DEFAULT_PLUGIN_SETTINGS.follow;
  expandOffsetX ??=
    renderInfo.useModal || ["top", "center", "bottom"].includes(pivot)
      ? 0
      : ["lt", "left", "lb"].includes(pivot) === follow
      ? -DEFAULT_PLUGIN_SETTINGS.expandOffsetX
      : DEFAULT_PLUGIN_SETTINGS.expandOffsetX;
  expandOffsetY ??=
    renderInfo.useModal || ["left", "right", "lt", "rt", "lb", "rb"].includes(pivot)
      ? 0
      : pivot === "center"
      ? DEFAULT_PLUGIN_SETTINGS.expandOffsetY
      : (pivot === "top") === follow
      ? -DEFAULT_PLUGIN_SETTINGS.expandOffsetY
      : DEFAULT_PLUGIN_SETTINGS.expandOffsetY;

  const updatedRenderInfo = {
    ...renderInfo,
    w,
    h,
    iconW,
    iconH,
    pivot,
    follow,
    expandOffsetX,
    expandOffsetY,
    renderFilter: getNodeFilter(nodeConstraint),
  };

  // This effect handles callbacks that dynamically render the plugin's position
  useLayoutEffect(() => {
    const updateFloating = async (e: any) => {
      const _iconW = iconW!;
      const _iconH = iconH!;
      const _pivot = pivot!;
      const _follow = follow!;
      const _offsetX =
        offsetX ??
        (["top", "center", "bottom"].includes(_pivot)
          ? 0
          : ["lt", "left", "lb"].includes(_pivot) === _follow
          ? -DEFAULT_PLUGIN_SETTINGS.offsetX
          : DEFAULT_PLUGIN_SETTINGS.offsetX);
      const _offsetY =
        offsetY ??
        (["left", "center", "right"].includes(_pivot)
          ? 0
          : ["lt", "top", "rt"].includes(_pivot) === _follow
          ? -DEFAULT_PLUGIN_SETTINGS.offsetY
          : DEFAULT_PLUGIN_SETTINGS.offsetY);
      // adjust floating
      const domFloating = document.querySelector<HTMLDivElement>(`#${_id}`);
      if (!domFloating) return;
      let x, y;
      if (!_follow) {
        const { x: left, y: top } = useBoardContainerLeftTop();
        const { w: bw, h: bh } = useBoardContainerWH();
        // x
        if (["lt", "left", "lb"].includes(_pivot)) {
          x = left + _offsetX;
        } else if (["rt", "right", "rb"].includes(_pivot)) {
          x = left + bw - _iconW + _offsetX;
        } else {
          x = left + 0.5 * (bw - _iconW) + _offsetX;
        }
        // y
        if (["lt", "top", "rt"].includes(_pivot)) {
          y = top + _offsetY;
        } else if (["lb", "bottom", "rb"].includes(_pivot)) {
          y = top + bh - _iconH + _offsetY;
        } else {
          y = top + 0.5 * (bh - _iconH) + _offsetY;
        }
      } else {
        const info = useSelecting("raw");
        if (DEBUG_PREFIX && _id.startsWith(DEBUG_PREFIX)) {
          console.log("> e", e);
          console.log("> info", _id, shallowCopy(info));
        }
        if (!info || (updatedRenderInfo.renderFilter && !updatedRenderInfo.renderFilter(info))) {
          return;
        }
        const bounding = info.displayNode
          ? info.displayNode.bbox.bounding
          : new INodes(info.nodes).bbox;
        const domPivot = boardBBoxToDom(bounding).pivot(_pivot);
        let offsetX, offsetY;
        // x
        if (["lt", "left", "lb"].includes(_pivot)) {
          offsetX = -_iconW + _offsetX;
        } else if (["rt", "right", "rb"].includes(_pivot)) {
          offsetX = _offsetX;
        } else {
          offsetX = -0.5 * _iconW + _offsetX;
        }
        // y
        if (["lt", "top", "rt"].includes(_pivot)) {
          offsetY = -_iconH + _offsetY;
        } else if (["lb", "bottom", "rb"].includes(_pivot)) {
          offsetY = _offsetY;
        } else {
          offsetY = -0.5 * _iconH + _offsetY;
        }
        ({ x, y } = domPivot.add(new Coordinate(offsetX, offsetY)));
      }
      domFloating.dataset.x = x.toString();
      domFloating.dataset.y = y.toString();
      domFloating.style.transform = `matrix(1,0,0,1,${x},${y})`;
      // adjust expand of the floating
      const domFloatingExpand = document.querySelector<HTMLDivElement>(`#${getExpandId(_id)}`);
      if (!domFloatingExpand) return;
      const { x: ex, y: ey } = getExpandPosition(updatedRenderInfo.useModal ?? false, {
        x,
        y,
        w,
        h,
        iconW: _iconW,
        iconH: _iconH,
        pivot: _pivot,
        follow: _follow,
        expandOffsetX: expandOffsetX!,
        expandOffsetY: expandOffsetY!,
      });
      domFloatingExpand.style.transform = `matrix(1,0,0,1,${ex},${ey})`;
    };
    const onFloatingReRender = ({ id: renderedId, needRender }: IFloatingRenderEvent) => {
      if (_id === renderedId && needRender) {
        updateFloating({ event: "rerender", needRender });
      }
    };
    const { dispose } = floatingRenderEvent.on(onFloatingReRender);
    injectNodeTransformEventCallback(_id, updateFloating);
    useSelectHooks().register({ key: _id, after: updateFloating });
    window.addEventListener("resize", updateFloating);
    if (useIsReady()) {
      updateFloating({ event: "init" });
    }

    return () => {
      if (DEBUG_PREFIX && _id.startsWith(DEBUG_PREFIX)) {
        console.log(">>>>> clean up");
      }
      dispose();
      removeNodeTransformEventCallback(_id);
      useSelectHooks().remove(_id);
      window.removeEventListener("resize", updateFloating);
    };
  }, [
    _id,
    iconW,
    iconH,
    nodeConstraint,
    pivot,
    follow,
    offsetX,
    offsetY,
    expandOffsetX,
    expandOffsetY,
    JSON.stringify(props),
    useIsReady(),
  ]);

  return (
    <Floating id={_id} ref={containerRef} renderInfo={updatedRenderInfo} {...props}>
      {children}
    </Floating>
  );
}) as ChakraComponent<"div", {}>;

export default observer(Render);
