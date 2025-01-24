import { useMemo } from "react";
import { useQuery } from "@tanstack/react-query";
import { MARKERS } from "@/core/constants";
import useMarking from "@/hooks/useMarking";
import { useImageStore } from "@/store/display";

const useMarkCanvas = () => {
  const { data: processImageData } = useQuery({
    queryKey: ["processedImageData"],
  });

  const {
    state: { marks },
    action: { onMark },
  } = useMarking();

  const imageRef = useImageStore((state) => state.imageRef);
  const rect = useMemo(
    () => imageRef?.current?.getBoundingClientRect(),
    [imageRef],
  );

  const circles = useMemo(() => {
    if (!processImageData?.defect_batches || !rect) return [];
    return processImageData.defect_batches
      .flatMap((defect_batch) => defect_batch.defect_files)
      .map((file) => {
        const dx = Math.round(file.norm_x_center * rect.width * 100) / 100;
        const dy = Math.round(file.norm_y_center * rect.height * 100) / 100;
        const stored_mark =
          marks.find((mark) => mark.file_name === file.file_name) ||
          marks.find(
            (mark) =>
              mark.file_name === file.file_name &&
              mark.file_name === file.file_name + MARKERS.zoom.name,
          );
        return {
          id: file.file_name,
          cx: dx,
          cy: dy,
          r: stored_mark?.marker.radius || MARKERS.temp.radius,
          color: stored_mark?.marker.color || MARKERS.temp.color,
        };
      });
  }, [processImageData, marks, rect]);

  return {
    state: { circles },
    action: { onMark },
  };
};

export default useMarkCanvas;
