import { MARKERS } from "../constants/markers";

const useMarkCanvas = (moveActive, marks, setMarks, markColor) => {
  const colorMarkers = markColor || [MARKERS.static];

  const resetMarks = () => setMarks([]);

  const addMark = (id, marker = MARKERS.zoom) => {
    setMarks(
      marks.some((mark) => mark.id === id) ? marks : [...marks, { id, marker }],
    );
  };

  const removeMark = (id) => {
    setMarks(marks.filter((mark) => mark.id != id));
  };

  const updateMark = (id, marker) => {
    setMarks(
      marks.map((mark) => (mark.id === id ? { ...mark, marker } : mark)),
    );
  };

  const handleMark = (e) => {
    if (moveActive) return;
    const id = e.currentTarget.id;
    const existingMark = marks.find((mark) => mark.id === id);
    if (!existingMark) addMark(id, colorMarkers[0]);
    else if (existingMark?.marker?.color === colorMarkers.at(-1).color)
      removeMark(id);
    else {
      const currentColorIndex = colorMarkers.findIndex(
        (color) => color?.color === existingMark?.marker?.color,
      );
      updateMark(id, colorMarkers[currentColorIndex + 1]);
    }
  };

  return {
    action: { resetMarks, addMark, removeMark, handleMark },
  };
};

export default useMarkCanvas;
