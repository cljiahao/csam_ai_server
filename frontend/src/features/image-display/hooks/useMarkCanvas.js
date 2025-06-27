import { useMemo } from "react";
import { useQuery } from "@tanstack/react-query";
import { MARKERS } from "@/core/constants";
import useMarking from "@/hooks/useMarking";
import { useImageStore } from "@/store/display";
import { useEffect, useState } from "react";

const useMarkCanvas = () => {
  const { data: processImageData } = useQuery({
    queryKey: ["processedImageData"],
  });

  const {
    state: { marks },
    action: { onMark },
  } = useMarking();

  const imageRef = useImageStore((state) => state.imageRef);

  // Using useState and useEffect to track image dimensions
  const [rect, setRect] = useState(imageRef?.current?.getBoundingClientRect());

  // Update rect when window resizes
  useEffect(() => {
    const handleResize = () => {
      if (imageRef?.current) {
        setRect(imageRef.current.getBoundingClientRect());
      }
    };

    window.addEventListener("resize", handleResize);

    // Clean up the event listener
    return () => {
      window.removeEventListener("resize", handleResize);
    };
  }, [imageRef]); // This effect depends on imageRef

  const circles = useMemo(() => {
    if (!processImageData?.file_data_batches || !rect) return [];

    // Create a map for faster lookup of stored marks
    const marksMap = new Map();
    marks.forEach((mark) => {
      marksMap.set(mark.file_name, mark);
      marksMap.set(mark.file_name + MARKERS.zoom.name, mark);
    });

    return processImageData.file_data_batches
      .flatMap((defect_batch) => defect_batch.data_files)
      .map((file) => {
        const dx = Math.round(file.norm_x_center * rect.width * 100) / 100;
        const dy = Math.round(file.norm_y_center * rect.height * 100) / 100;

        const stored_mark =
          marksMap.get(file.file_name) ||
          marksMap.get(file.file_name + MARKERS.zoom.name);

        return {
          id: file.file_name,
          cx: dx,
          cy: dy,
          r: stored_mark?.marker.radius || MARKERS.temp.radius,
          color: stored_mark?.marker.color || MARKERS.temp.color,
        };
      });
  }, [processImageData, marks, rect]); // Only recompute when these change

  return {
    state: { circles },
    action: { onMark },
  };
};

export default useMarkCanvas;
