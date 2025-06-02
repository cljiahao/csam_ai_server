import { useShallow } from "zustand/react/shallow";
import { MARKERS, ZOOM_SCALE } from "@/core/constants";
import { useCoordStores, useImageStore } from "@/store/display";
import useMarking from "@/hooks/useMarking";
import { useQueryImageData } from "../api/gallery";

const useThumbnailHandlers = () => {
  const imageData = useQueryImageData();

  const {
    state: { marks },
    action: { onMark, addMark, removeMark },
  } = useMarking();

  const marksFileNames = new Set(marks.map((mark) => mark.file_name));

  const imageRef = useImageStore((state) => state.imageRef);
  const { updateCoords, updateScale, resetCoords } = useCoordStores(
    useShallow((state) => ({
      updateCoords: state.updateCoords,
      updateScale: state.updateScale,
      resetCoords: state.resetCoords,
    })),
  );

  // Handler to focus on the element
  function onFocus(e) {
    const file_name = e.currentTarget.id;
    const focus_item = imageData?.file_data_batches?.reduce(
      (found, defect_batch) => {
        if (found) return found; // If already found, skip further checks
        return (
          defect_batch.defect_records.find(
            (file) => file.file_name === file_name,
          ) || null
        );
      },
      null,
    );
    const rect = imageRef.current.getBoundingClientRect();
    const dx =
      (1 / 2 - focus_item.norm_x_center) * rect.width * ZOOM_SCALE.focus;
    const dy =
      (1 / 2 - focus_item.norm_y_center) * rect.height * ZOOM_SCALE.focus;
    updateCoords(dx, dy);
    updateScale(ZOOM_SCALE.focus);
    addMark(file_name + MARKERS.zoom.name, MARKERS.zoom);
  }

  // Handler to unfocus element
  function unFocus(e) {
    const file_name = e.currentTarget.id;
    resetCoords();
    removeMark(file_name + MARKERS.zoom.name);
  }

  return {
    state: { imageData, marksFileNames },
    action: { onFocus, unFocus, onMark },
  };
};

export default useThumbnailHandlers;
