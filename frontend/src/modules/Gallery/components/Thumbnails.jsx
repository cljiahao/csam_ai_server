import { MARKERS } from "@/core/config";
import { Button } from "@/components/ui/button";
import {
  useCanvasContext,
  useDisplayContext,
  useImageDetailsContext,
} from "@/contexts/context";
import { useFocus, useMarker } from "../hooks";

const Thumbnails = ({ page, thumbs_array }) => {
  const { resetZoom } = useDisplayContext();
  const { marks, coordNormalize, updateMarkSelected } = useCanvasContext();
  const { imageDetails } = useImageDetailsContext();
  const [focusOnElement] = useFocus();
  const [updateMarkViewing, resetMarkViewing] = useMarker();

  // Function to check if thumbnail is changing to default
  function isChangingToDefault(e) {
    const { id: file_name } = e.currentTarget;
    return marks.some(
      ({ id, circle }) =>
        id === file_name && circle?.id === MARKERS.marks.length - 1,
    );
  }

  // Function to check if thumbnail is default
  function isDefault(file_name) {
    return marks.some(({ id, circle }) => id === file_name && circle?.id === 0);
  }

  // Handler to focus on the element
  function onFocus(e) {
    const file_name = e.currentTarget.id;
    const norm_coords = coordNormalize({ file_name });
    focusOnElement({ norm_coords });
    updateMarkViewing(e);
  }

  // Handler to unfocus element
  function unFocus() {
    resetMarkViewing();
    resetZoom();
  }

  // Handler for thumbnail click
  function onThumbnailClick(e) {
    updateMarkSelected(e);
    page.toUpperCase() === "CDC" && isChangingToDefault(e)
      ? unFocus()
      : onFocus(e);
  }

  return (
    <div className="hw-full grid grid-cols-8 gap-3">
      {thumbs_array.map((file_name) => {
        const folder =
          file_name[0] === "0"
            ? "temp"
            : MARKERS.marks.find(({ id }) => id == file_name[0]).name;
        return (
          <Button
            key={file_name}
            id={file_name}
            className={`hw-full border-2 p-0 ${isDefault(file_name) ? "" : "border-red-500"}`}
            onMouseEnter={onFocus}
            onMouseLeave={unFocus}
            onClick={onThumbnailClick}
          >
            <img
              src={`/api/image/${imageDetails.directory}/${folder}/${file_name}`}
              alt={file_name}
              className="hw-full"
            />
          </Button>
        );
      })}
    </div>
  );
};

export default Thumbnails;
