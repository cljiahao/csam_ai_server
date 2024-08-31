import { useCanvasContext } from "@/contexts/csamContext";
import { useEffect, useState, useMemo } from "react";

const useImageInfo = (mode) => {
  const { marks, markers } = useCanvasContext();
  const [fileNames, setFileNames] = useState({});

  const imageInfo = useMemo(() => {
    return marks?.reduce((acc, { batch, id, circle }) => {
      if (markers.zoom !== circle) {
        if (!acc[batch]) {
          acc[batch] = [];
        }
        if (
          markers.marks.find(({ id: markerId }) => markerId === 0) === circle &&
          mode.toUpperCase() === "CDC"
        )
          return acc;
        acc[batch].push(id);
      }
      return acc;
    }, {});
  }, [marks, markers, mode]);

  useEffect(() => {
    setFileNames(imageInfo);
  }, [imageInfo]);

  return { fileNames };
};

export default useImageInfo;
