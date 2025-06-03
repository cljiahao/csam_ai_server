import { useCallback, useState } from "react";

import { MARKERS } from "../constants/markers";

const useMarkCanvas = () => {
  const [marks, setMarks] = useState([]);

  const resetMarks = () => setMarks([]);
  const addMark = (fileName, marker) =>
    setMarks((prevMarks) =>
      prevMarks.some((mark) => mark.fileName === fileName)
        ? prevMarks
        : [...prevMarks, { fileName, marker }],
    );
  const removeMark = (fileName) =>
    setMarks((prevMarks) =>
      prevMarks.filter((mark) => mark.fileName != fileName),
    );
  const updateMark = (fileName, marker) =>
    setMarks((prevMarks) =>
      prevMarks.map((mark) =>
        mark.fileName === fileName ? { ...mark, marker } : mark,
      ),
    );

  const handleMark = useCallback(
    (e) => {
      const fileName = e.currentTarget.id;
      const existingMark = marks.find((mark) => mark.fileName === fileName);

      if (!existingMark) addMark(fileName, MARKERS.color[0]);
      else if (existingMark.marker === MARKERS.color.at(-1))
        removeMark(fileName);
      else {
        const currentColorIndex = MARKERS.color.findIndex(
          (color) => color === existingMark.marker,
        );
        updateMark(fileName, MARKERS.color[currentColorIndex + 1]);
      }
    },
    [marks],
  );

  return {
    state: { marks },
    action: { resetMarks, addMark, handleMark },
  };
};

export default useMarkCanvas;
