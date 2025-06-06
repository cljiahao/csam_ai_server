import { useIsMutating } from "@tanstack/react-query";
import { useShallow } from "zustand/react/shallow";

import { MUTATION_KEYS } from "@/constants/api-keys";
import { useImageStore } from "@/store/image";
import useMarksStore from "@/store/marks";
import { useQueryColorData, useQueryImageData } from "../api/image-display";

const useImageDisplay = () => {
  const { imageRef, error, image } = useImageStore(
    useShallow((state) => ({
      imageRef: state.imageRef,
      error: state.error,
      image: state.image,
    })),
  );

  const { markRef, marks, setMarks } = useMarksStore(
    useShallow((state) => ({
      markRef: state.markRef,
      marks: state.marks,
      setMarks: state.setMarks,
    })),
  );

  const colorData = useQueryColorData();
  const markColor = colorData?.map((state) => ({ ...state, radius: 1 }));

  const imageData = useQueryImageData();
  const coordinates = imageData?.file_data_batches.flatMap(
    (batch) => batch.defect_records,
  );

  const isMutating = useIsMutating({
    mutationKey: [MUTATION_KEYS.API_IMAGE_DATA],
  });

  return {
    state: {
      imageRef,
      markRef,
      error,
      image,
      marks,
      markColor,
      coordinates: coordinates,
      isLoading: isMutating > 0,
    },
    action: { setMarks },
  };
};

export default useImageDisplay;
