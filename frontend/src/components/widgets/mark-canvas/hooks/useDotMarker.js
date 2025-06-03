import { useMemo } from "react";

import { MARKERS } from "../constants/markers";

const useDotMarker = (imageSize, marks, coordinates) => {
  const generateCircles = useMemo(() => {
    if (!imageSize || !coordinates) return [];

    const marksMap = new Map();
    marks.forEach((mark) => {
      marksMap.set(mark.fileName, mark);
      marksMap.set(mark.file_name + MARKERS.zoom.name, mark);
    });

    return (coordinates || []).map((file, index) => {
      const dx = Math.round(file.norm_x_center * imageSize.width * 100) / 100;
      const dy = Math.round(file.norm_y_center * imageSize.height * 100) / 100;

      const stored_mark =
        marksMap.get(file.file_name) ||
        marksMap.get(file.file_name + MARKERS.zoom.name);

      return {
        id: index,
        cx: dx,
        cy: dy,
        r: stored_mark?.marker.radius || MARKERS.static.radius,
        color: stored_mark?.marker.color || MARKERS.static.color,
      };
    });
  }, [coordinates, marks, imageSize]);

  return { state: { generateCircles } };
};

export default useDotMarker;
