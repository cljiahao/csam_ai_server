import { useCallback, useEffect } from "react";
import { useCanvasContext, useImageDetailsContext } from "@/contexts/context";
import { useFetch } from "@/hooks/useFetch";
import { uploadImage } from "@/services/api_files";
import { useInfoBarContext } from "@/modules/InfoBar/contexts/infoBarContext";

const useLoadImage = () => {
  const { data, error, isLoading, fetchData } = useFetch();
  const { updateMarks, updateImageSize } = useCanvasContext();
  const { updateImageDetails } = useImageDetailsContext();
  const { updateInfoDetails } = useInfoBarContext();

  useEffect(() => {
    if (data) {
      updateImageDetails(data);
      if (!isLoading) {
        updateMarks(data.chips);
      }
    }
  }, [data, isLoading, updateImageDetails]); // eslint-disable-line react-hooks/exhaustive-deps

  useEffect(() => {
    updateImageDetails({ isLoading });
  }, [isLoading, updateImageDetails]);

  useEffect(() => {
    if (error) {
      updateImageDetails(error);
    }
  }, [error, updateImageDetails]);

  const getProcessedImage = useCallback(
    (mode, file, inputFormData) => {
      // Update image size to calculate canvas marks
      updateImageSize(file);

      // To backend for processing and return predictions
      const formData = new FormData();
      formData.append("file", file);
      fetchData(
        () =>
          uploadImage(
            formData,
            mode.toUpperCase(),
            inputFormData.lotNo,
            inputFormData.item,
          ),
        true,
      );

      // Update plate number using file name
      updateInfoDetails({
        plate: file?.name.split(".").slice(0, -1).join("."),
      });
    },
    [fetchData, updateImageSize, updateInfoDetails],
  );

  return getProcessedImage;
};

export default useLoadImage;
