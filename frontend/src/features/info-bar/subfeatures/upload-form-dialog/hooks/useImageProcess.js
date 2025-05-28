import { useState } from "react";
import { useImageStore } from "@/store/display";
import { useShallow } from "zustand/react/shallow";
import { useMutation, useQueryClient } from "@tanstack/react-query";

import useMarking from "@/hooks/useMarking";
import { uploadImage } from "@/services/api_csam_image";
import { useColorStore } from "@/store/color";

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
      queryClient.removeQueries(["processedImageData"]);
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

  const setColors = useColorStore((state) => state.setColors);

  const { mutateAsync: processImage } = useImageMutation({ setError });

  const handleImageProcess = (mode, item, lotNo, file, colors) => {
    setColors(colors);

    const formData = new FormData();
    formData.append("file", file);
    processImage(
      { mode, item, lotNo, formData, colors },
      {
        onSuccess: (data) => {
          if (data) {
            setImage(file);
            const filteredDefectFiles = data.file_data_batches.flatMap(
              (batch) =>
                batch.defect_records
                  .filter((file) => file.defect_mode !== "temp")
                  .map((file) => ({
                    file_name: file.file_name,
                    defect_mode: file.defect_mode,
                  })),
            );
            filteredDefectFiles.forEach(({ file_name, defect_mode }) => {
              const colorObj = colors.find(
                (color) => color.defect_label === defect_mode,
              );
              if (!colorObj) return;
              addMark(file_name, {
                name: colorObj.defect_label,
                color: colorObj.hex_color,
                radius: 1,
              });
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
