import { useCallback, useState } from "react";
import { MARKERS } from "@/core/config";
import { coordsExtract } from "@/lib/chipInfoExtract";

export function useMarkCanvas() {
  const [imageSize, setImageSize] = useState([]);
  const [marks, setMarks] = useState([]);

  const coordNormalize = useCallback(
    ({ xycoords, file_name }) => {
      let coords = file_name ? coordsExtract(file_name) : xycoords;
      return imageSize.map((dim, index) => coords[index] / dim);
    },
    [imageSize],
  );

  const updateImageSize = useCallback((file) => {
    const imageUrl = URL.createObjectURL(file);
    const image = new Image();

    image.onload = () => {
      setImageSize([image.width, image.height]);
      URL.revokeObjectURL(imageUrl); // Clean up the object URL
    };

    image.src = imageUrl;
  }, []);

  const updateMarks = (chip_details) => {
    const updatedMarks = Object.entries(chip_details).flatMap(
      ([batch, file_names]) =>
        file_names.map((file_name) => {
          const [norm_x, norm_y] = coordNormalize({ file_name });
          const default_circle = MARKERS.marks.find(
            ({ id }) => id == file_name[0],
          );
          return {
            id: file_name,
            batch: batch,
            norm_x: norm_x,
            norm_y: norm_y,
            circle: default_circle,
          };
        }),
    );
    setMarks(updatedMarks);
  };

  const updateMarkSelected = useCallback(
    (e) => {
      const file_name = e.currentTarget.id;
      const toUpdate = marks.find(({ id }) => id === file_name);
      const updateCircle = MARKERS.marks.find(
        ({ id }) => id === (toUpdate.circle.id + 1) % MARKERS.marks.length,
      );
      const update_marks = marks.map((mark) =>
        mark.id === file_name ? { ...mark, circle: updateCircle } : mark,
      );
      setMarks([...update_marks]);
    },
    [marks],
  );

  return {
    marks,
    setMarks,
    coordNormalize,
    updateImageSize,
    updateMarks,
    updateMarkSelected,
  };
}
