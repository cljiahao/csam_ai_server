import { useCallback, useRef, useState } from "react";
import { ZOOM_SCALE } from "../constants/zoom-scale";

export const usePanZoom = () => {
  const [coords, setCoords] = useState({ x: 0, y: 0 });
  const [scale, setScale] = useState(1);
  const [moveActive, setMoveActive] = useState(false);

  const displayRef = useRef();
  const panZoomRef = useRef({
    oldX: 0,
    oldY: 0,
    panActive: false,
  });

  const updateCoords = (x, y) => setCoords({ x, y });
  const updateScale = (newScale) => setScale(newScale);
  const resetCoords = () => {
    setCoords({ x: 0, y: 0 });
    setScale(1);
    setMoveActive(false);
  };

  const handlePan = useCallback(
    (e) => {
      e.preventDefault();
      if (e.type === "mousedown") {
        panZoomRef.current = {
          oldX: e.clientX,
          oldY: e.clientY,
          panActive: true,
        };
        setMoveActive(false);
      } else if (e.type === "mouseup") {
        panZoomRef.current.panActive = false;
      } else if (e.type === "mousemove") {
        if (panZoomRef.current.panActive) {
          if (!moveActive) setMoveActive(true);
          const dx = coords.x + e.clientX - panZoomRef.current.oldX;
          const dy = coords.y + e.clientY - panZoomRef.current.oldY;
          updateCoords(dx, dy);

          panZoomRef.current = {
            ...panZoomRef.current,
            oldX: e.clientX,
            oldY: e.clientY,
          };
        }
      }
    },
    [coords, moveActive],
  );

  const onWheel = useCallback(
    (e) => {
      if (e.deltaY && displayRef.current) {
        if (scale >= 1) {
          const sign = Math.sign(e.deltaY) / ZOOM_SCALE.scroll;
          const factor = 1 - sign;
          const rect = displayRef.current.getBoundingClientRect();
          const dx = coords.x + (e.clientX - rect.width / 2 - coords.x) * sign;
          const dy = coords.y + (e.clientY - rect.height / 2 - coords.y) * sign;
          updateCoords(dx, dy);
          updateScale(scale * factor);
        } else {
          resetCoords();
        }
      }
    },
    [displayRef, coords, scale],
  );

  return {
    state: { ...coords, scale, displayRef, moveActive },
    action: { updateCoords, updateScale, resetCoords, handlePan, onWheel },
  };
};
