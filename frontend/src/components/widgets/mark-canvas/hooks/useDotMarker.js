import { useMemo } from "react";

import { MARKERS } from "../constants/markers";
import { useMarkCanvasContext } from "../context/MarkCanvasContext";

const useDotMarker = () => {
  const { imageSize, marks, coordinates, showStatic } = useMarkCanvasContext();

  const generateCircles = useMemo(() => {
    if (!imageSize || !coordinates) return [];

    const marksMap = new Map();
    marks?.forEach((mark) => {
      marksMap.set(mark.id, mark);
      marksMap.set(mark.id + MARKERS.zoom.name, mark);
    });

    return (coordinates || []).map((file) => {
      const dx = Math.round(file.norm_x_center * imageSize.width * 100) / 100;
      const dy = Math.round(file.norm_y_center * imageSize.height * 100) / 100;

      const stored_mark =
        marksMap.get(file.id) || marksMap.get(file.id + MARKERS.zoom.name);

      return {
        id: file.id,
        cx: dx,
        cy: dy,
        r:
          stored_mark?.marker?.radius ||
          (showStatic ? MARKERS.static.radius : MARKERS.temp.radius),
        color:
          stored_mark?.marker?.color ||
          (showStatic ? MARKERS.static.color : MARKERS.temp.color),
      };
    });
  }, [imageSize, marks, coordinates, showStatic]);

  return { state: { generateCircles } };
};

export default useDotMarker;
