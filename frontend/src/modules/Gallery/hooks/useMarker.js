import { MARKERS } from "@/core/config";
import { useCanvasContext } from "@/contexts/context";

export function useMarker() {
  const { marks, setMarks } = useCanvasContext();

  function updateMarkViewing(e) {
    const { id: fileName } = e.currentTarget;
    // Check if the zoomed mark already exists
    const zoomedMarkId = fileName + "_zoom";
    const existingZoomMark = marks.find(({ id }) => id === zoomedMarkId);

    if (!existingZoomMark) {
      const fileToZoom = marks.find(({ id }) => id === fileName);
      setMarks((prevMark) => [
        ...prevMark,
        { ...fileToZoom, id: zoomedMarkId, circle: MARKERS.zoom },
      ]);
    }
  }

  function resetMarkViewing() {
    setMarks((prevMarks) =>
      prevMarks.filter(({ circle }) => circle !== MARKERS.zoom),
    );
  }

  return [updateMarkViewing, resetMarkViewing];
}
