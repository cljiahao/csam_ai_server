import { useImageStore } from "@/store/display";
import { useState } from "react";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { uploadImage } from "@/services/api_files";
import { useShallow } from "zustand/react/shallow";
import useMarking from "@/hooks/useMarking";
import { MARKERS } from "@/core/constants";

const useImageMutation = ({ setError }) => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationKey: ["imageProcess"],
    mutationFn: async ({ mode, item, lotNo, formData }) =>
      await uploadImage(mode, item, lotNo, formData),
    onSuccess: (data) => {
      queryClient.setQueryData(["processedImageData"], data);
    },
    onError: (error) => {
      console.log(error.message);
      setError(error.message);
      queryClient.removeQueries(["processedImageData"]); // Clear cache on error
    },
  });
};

const useImageProcess = () => {
  const [isDialogOpen, setDialogOpen] = useState();
  const {
    action: { addMark },
  } = useMarking();
  const { setImage, setError } = useImageStore(
    useShallow((state) => ({
      setImage: state.setImage,
      setError: state.setError,
    })),
  );

  const { mutate: processImage } = useImageMutation({ setError });

  const handleImageProcess = (mode, item, lotNo, file) => {
    const formData = new FormData();
    formData.append("file", file);
    processImage(
      { mode, item, lotNo, formData },
      {
        onSuccess: (data) => {
          if (data) {
            setImage(file);
            const filteredDefectFiles = data.defect_batches.flatMap((batch) =>
              batch.defect_files
                .filter((file) => file.defect_mode !== "temp") // Filter out 'temp' defect_mode
                .map((file) => ({
                  file_name: file.file_name,
                  defect_mode: file.defect_mode,
                })),
            );
            filteredDefectFiles.forEach(({ file_name, defect_mode }) => {
              addMark(
                file_name,
                MARKERS.colors.find((color) => color.name === defect_mode),
              );
            });
          }
        },
      },
    );
  };

  return {
    state: { isDialogOpen },
    action: { setDialogOpen, handleImageProcess },
  };
};

export default useImageProcess;
