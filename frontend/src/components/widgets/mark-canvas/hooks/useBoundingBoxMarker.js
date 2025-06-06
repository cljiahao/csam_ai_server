import { useMemo } from "react";

import { MARKERS } from "../constants/markers";
import { useMarkCanvasContext } from "../context/MarkCanvasContext";

const useBoundingBoxMarker = () => {
  const { imageSize, marks, coordinates, showStatic } = useMarkCanvasContext();

  const generateRectangles = useMemo(() => {
    if (!imageSize || !coordinates) return [];

    const marksMap = new Map();
    marks.forEach((mark) => {
      marksMap.set(mark.id, mark);
      marksMap.set(mark.id + MARKERS.zoom.name, mark);
    });

    return (coordinates || []).map((file) => {
      const dx =
        Math.round(
          (file.norm_x_center - file.norm_batch_width / 2) *
            imageSize.width *
            100,
        ) / 100;
      const dy =
        Math.round(
          (file.norm_y_center - file.norm_batch_height / 2) *
            imageSize.height *
            100,
        ) / 100;
      const d_width =
        Math.round(file.norm_batch_width * imageSize.width * 100) / 100;
      const d_height =
        Math.round(file.norm_batch_height * imageSize.height * 100) / 100;

      const stored_mark =
        marksMap.get(file.id) || marksMap.get(file.id + MARKERS.zoom.name);

      return {
        id: file.id,
        x_start: dx,
        y_start: dy,
        width: d_width,
        height: d_height,
        thickness:
          stored_mark?.marker.radius ||
          (showStatic ? MARKERS.static.radius : MARKERS.temp.radius),
        color:
          stored_mark?.marker.color ||
          (showStatic ? MARKERS.static.color : MARKERS.temp.color),
      };
    });
  }, [imageSize, marks, coordinates, showStatic]);

  return { state: { generateRectangles } };
};

export default useBoundingBoxMarker;
