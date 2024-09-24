import { useEffect } from "react";
import { useFetch } from "@/hooks/useFetch";
import { getProcessedCount } from "@/services/api_retrieve";
import { useInfoBarContext } from "@/modules/InfoBar/contexts/infoBarContext";
import { useImageDetailsContext } from "@/contexts/context";

const useInfoCount = (page) => {
  const { data, error, isLoading, fetchData } = useFetch();
  const { imageDetails } = useImageDetailsContext();
  const { infoDetails } = useInfoBarContext();

  useEffect(() => {
    const fetchProcessedCount = () => {
      if (imageDetails.chips && infoDetails.item) {
        fetchData(
          () => getProcessedCount(page, infoDetails.lotNo, infoDetails.plate),
          true,
        );
      }
    };
    fetchProcessedCount();
  }, [infoDetails, imageDetails.chips, page, fetchData]);

  return { data, error, isLoading };
};

export default useInfoCount;
