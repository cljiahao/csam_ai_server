import { useState } from "react";
import { useShallow } from "zustand/react/shallow";

import { useImageDataMutation } from "@/features/info-bar/api/info-bar";
import useMarking from "@/hooks/useMarking";
import { useColorStore } from "@/store/marks";
import { useImageStore } from "@/store/image";

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

  const { mutateAsync: processImage } = useImageDataMutation(setError);

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
