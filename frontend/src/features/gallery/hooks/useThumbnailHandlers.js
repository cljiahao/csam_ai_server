import { useQueryImageData } from "../api/gallery";
import useMarksStore from "@/store/marks";
import useImageStore from "@/store/image";
import { useShallow } from "zustand/react/shallow";

const useThumbnailHandlers = () => {
  const { markRef, marks } = useMarksStore(
    useShallow((state) => ({ markRef: state.markRef, marks: state.marks })),
  );
  const imageRef = useImageStore((state) => state.imageRef);

  const marksID = new Set(marks.map((mark) => mark?.id));

  const imageData = useQueryImageData();

  // Handler to focus on the element
  function onFocus(e) {
    const id = e.currentTarget.id;
    const focus_item = imageData?.file_data_batches?.reduce(
      (found, defect_batch) => {
        if (found) return found; // If already found, skip further checks
        return (
          defect_batch?.defect_records.find((file) => file?.id === id) || null
        );
      },
      null,
    );
    const centerX = focus_item?.norm_x_center;
    const centerY = focus_item?.norm_y_center;
    imageRef?.current?.zoomFocus(centerX, centerY);
    markRef?.current?.addMark(focus_item?.id + "mark");
  }

  // Handler to unfocus element
  function unFocus(e) {
    const id = e.currentTarget.id;
    imageRef?.current?.resetCoords();
    markRef?.current?.removeMark(id + "mark");
  }

  const onClick = (e) => markRef?.current?.handleMark(e);

  return {
    state: { imageData, marksID },
    action: { onFocus, unFocus, onClick },
  };
};

export default useThumbnailHandlers;
