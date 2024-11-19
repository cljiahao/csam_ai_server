import { useCallback, useState } from "react";

const defaultImageDetails = {
  image: "",
  chips: null,
  directory: "",
  detail: "",
  isLoading: false,
};

export function useImageDetails() {
  const [imageDetails, setImageDetails] = useState({ ...defaultImageDetails });

  const updateImageDetails = useCallback((amend_data) => {
    if (!amend_data) return;

    setImageDetails((prevImageDetails) => {
      const updatedDetails = { ...prevImageDetails };

      // Update only the keys that exist in prevImageDetails
      Object.keys(amend_data).forEach((key) => {
        if (key in prevImageDetails) {
          updatedDetails[key] = amend_data[key];
        }
      });

      return updatedDetails;
    });
  }, []);

  function refreshImageDetails() {
    setImageDetails({ ...defaultImageDetails });
  }

  return { imageDetails, updateImageDetails, refreshImageDetails };
}
