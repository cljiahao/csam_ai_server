import { useMemo } from "react";

import { MARKERS } from "../constants/markers";

const useBoundingBoxMarker = (imageSize, marks, coordinates) => {
  const generateRectangles = useMemo(() => {
    if (!imageSize || !coordinates) return [];

    const marksMap = new Map();
    marks.forEach((mark) => {
      marksMap.set(mark.fileName, mark);
      marksMap.set(mark.file_name + MARKERS.zoom.name);
    });

    return (coordinates || []).map((file, index) => {
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
        marksMap.get(file.file_name) ||
        marksMap.get(file.file_name + MARKERS.zoom.name);

      return {
        id: index,
        x_start: dx,
        y_start: dy,
        width: d_width,
        height: d_height,
        thickness: stored_mark?.marker.radius || MARKERS.static.radius,
        color: stored_mark?.marker.color || MARKERS.static.color,
      };
    });
  }, [coordinates, marks, imageSize]);

  return { state: { generateRectangles } };
};

export default useBoundingBoxMarker;
