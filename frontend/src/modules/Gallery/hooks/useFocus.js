import { ZOOM_SCALE } from "@/core/config";
import { useDisplayContext } from "@/contexts/context";

export function useFocus() {
  const { display, setDisplay } = useDisplayContext();

  function focusOnElement({ coords, norm_coords }) {
    const [xc, yc] = coords || [
      norm_coords[0] * display.width,
      norm_coords[1] * display.height,
    ];

    const x = (display.width / 2 - xc) * ZOOM_SCALE.focus;
    const y = (display.height / 2 - yc) * ZOOM_SCALE.focus;

    setDisplay((prevDisplay) => ({
      ...prevDisplay,
      x,
      y,
      scale: ZOOM_SCALE.focus,
    }));
  }

  return [focusOnElement];
}
