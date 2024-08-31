import { useEffect } from "react";
import { useFetch } from "@/hooks/useFetch";
import { getProcessedCount } from "@/services/api_retrieve";
import { useInfoBarContext } from "@/modules/InfoBar/contexts/infoBarContext";
import { useImageDetailsContext } from "@/contexts/csamContext";

const useInfoCount = ({ mode }) => {
  const { data, error, isLoading, fetchData } = useFetch();
  const { infoDetails } = useInfoBarContext();
  const { imageDetails } = useImageDetailsContext();

  useEffect(() => {
    const fetchProcessedCount = () => {
      if (imageDetails.chips) {
        fetchData(
          () => getProcessedCount(mode, infoDetails.lotNo, infoDetails.plate),
          true,
        );
      }
    };
    fetchProcessedCount();
  }, [mode, infoDetails, imageDetails.chips, fetchData]);

  return { data, error, isLoading };
};

export default useInfoCount;
