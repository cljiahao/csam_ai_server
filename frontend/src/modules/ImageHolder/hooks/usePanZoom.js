import { ZOOM_SCALE } from "@/core/config";
import { useDisplayContext } from "@/contexts/context";

export function usePanZoom() {
  const { display, setDisplay } = useDisplayContext();

  function onWheel(e) {
    if (e.deltaY) {
      if (display.scale >= 1) {
        const sign = Math.sign(e.deltaY) / ZOOM_SCALE.scroll;
        const scale = 1 - sign;
        setDisplay((prevDisplay) => ({
          ...prevDisplay,
          x:
            prevDisplay.x * scale -
            (prevDisplay.width / 2 - e.clientX + prevDisplay.x) * sign,
          y:
            prevDisplay.y * scale -
            (prevDisplay.height / 2 - e.clientY + prevDisplay.y) * sign,
          scale: prevDisplay.scale * scale,
        }));
      } else
        setDisplay((prevDisplay) => ({ ...prevDisplay, x: 0, y: 0, scale: 1 }));
    }
  }

  function onPanning(e) {
    if (e.type === "mousedown") {
      setDisplay((prevDisplay) => ({
        ...prevDisplay,
        oldX: e.clientX,
        oldY: e.clientY,
        pan: true,
        move: false,
      }));
    } else if (e.type === "mouseup") {
      setDisplay((prevDisplay) => ({
        ...prevDisplay,
        pan: false,
      }));
    } else if (e.type === "mousemove" && display.pan) {
      setDisplay((prevDisplay) => ({
        ...prevDisplay,
        x: prevDisplay.x + e.clientX - prevDisplay.oldX,
        y: prevDisplay.y + e.clientY - prevDisplay.oldY,
        oldX: e.clientX,
        oldY: e.clientY,
        move: true,
      }));
    }
  }

  return [onWheel, onPanning];
}
