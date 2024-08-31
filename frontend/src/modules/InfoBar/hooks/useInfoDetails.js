import { useCallback, useState } from "react";

const defaultInfoDetails = {
  lotNo: "",
  plate: "",
  item: "",
};

const useInfoDetails = () => {
  const [infoDetails, setInfoDetails] = useState({ ...defaultInfoDetails });

  const updateInfoDetails = useCallback((amend_data) => {
    if (!amend_data) return;

    setInfoDetails((prevInfoDetails) => {
      const updatedDetails = { ...prevInfoDetails };

      // Update only the keys that exist in prevImageDetails
      Object.keys(amend_data).forEach((key) => {
        if (key in prevInfoDetails) {
          updatedDetails[key] = amend_data[key];
        }
      });

      return updatedDetails;
    });
  }, []);

  return { infoDetails, updateInfoDetails };
};

export default useInfoDetails;
