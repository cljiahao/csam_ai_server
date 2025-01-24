import { useCallback, useRef } from "react";
import { useShallow } from "zustand/react/shallow";

import { ZOOM_SCALE } from "@/core/constants";
import { useCoordStores, useImageStore } from "@/store/display";

export const usePanZoom = () => {
  const imageRef = useImageStore((state) => state.imageRef);

  // Extracting the state and actions from useDisplayStore
  const {
    x,
    y,
    scale,
    moveActive,
    updateCoords,
    updateScale,
    resetCoords,
    isMove,
  } = useCoordStores(
    useShallow((state) => ({
      x: state.x,
      y: state.y,
      scale: state.scale,
      moveActive: state.moveActive,
      updateCoords: state.updateCoords,
      updateScale: state.updateScale,
      resetCoords: state.resetCoords,
      isMove: state.isMove,
    })),
  );

  const panZoomRef = useRef({
    oldX: 0,
    oldY: 0,
    panActive: false,
  });

  const handlePan = useCallback(
    (e) => {
      e.preventDefault();
      switch (e.type) {
        case "mousedown":
          panZoomRef.current = {
            oldX: e.clientX,
            oldY: e.clientY,
            panActive: true,
          };
          isMove(false);
          break;
        case "mouseup":
          panZoomRef.current.panActive = false;
          break;
        case "mousemove":
          if (panZoomRef.current.panActive) {
            if (!moveActive) isMove(true);

            const dx = x + e.clientX - panZoomRef.current.oldX;
            const dy = y + e.clientY - panZoomRef.current.oldY;
            updateCoords(dx, dy);

            panZoomRef.current = {
              ...panZoomRef.current,
              oldX: e.clientX,
              oldY: e.clientY,
            };
          }
          break;
        default:
          break;
      }
    },
    [x, y, moveActive, isMove, updateCoords],
  );

  const onWheel = useCallback(
    (e) => {
      if (e.deltaY) {
        if (scale >= 1) {
          const sign = Math.sign(e.deltaY) / ZOOM_SCALE.scroll;
          const factor = 1 - sign;
          const rect = imageRef.current.getBoundingClientRect();
          const dx = x + (e.clientX - rect.width / 2 - x) * sign;
          const dy = y + (e.clientY - rect.height / 2 - y) * sign;
          updateCoords(dx, dy);
          updateScale(scale * factor);
        } else {
          resetCoords();
        }
      }
    },
    [imageRef, scale, x, y, updateCoords, updateScale, resetCoords],
  );

  return {
    state: { x, y, scale, moveActive },
    action: { handlePan, onWheel, resetCoords },
  };
};
