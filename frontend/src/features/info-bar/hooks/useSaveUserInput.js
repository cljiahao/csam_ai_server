import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";

import useMarking from "@/hooks/useMarking";
import { saveFinalJudgement } from "@/services/api_csam_image";
import useBaseStore from "@/store/base";

const useSaveUserMutation = ({ updateError }) => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationKey: ["saveUserInput"],
    mutationFn: async ({ mode, item, lotNo, data }) =>
      await saveFinalJudgement(mode, item, lotNo, data),
    onSuccess: (data) => {
      queryClient.setQueryData(["saveUserInput"], data);
    },
    onError: (error) => {
      console.log(error.message);
      updateError(error.message);
      queryClient.removeQueries(["saveUserInput"]); // Clear cache on error
    },
  });
};

const useSaveUserInput = () => {
  const updateError = useBaseStore((state) => state.updateError);
  const { data: processImageData } = useQuery({
    queryKey: ["processedImageData"],
  });

  const {
    state: { marks },
  } = useMarking();

  const { mutateAsync: processUserInput } = useSaveUserMutation({
    updateError,
  });

  const handleSaveUserInput = async ({ mode, item, lotNo }) => {
    const targetFileNames = new Map(
      marks.map((mark) => [mark.file_name, mark.marker.name]),
    );

    const userInputData = {
      ...processImageData,
      file_data_batches: processImageData?.file_data_batches
        .map((batch) => ({
          ...batch,
          defect_records: batch.defect_records.reduce((result, file) => {
            if (targetFileNames.has(file.file_name)) {
              result.push({
                ...file,
                defect_mode: targetFileNames.get(file.file_name),
              });
            }
            return result;
          }, []),
        }))
        .filter((batch) => batch.defect_records?.length > 0), // Remove batches with no files
    };
    if (processImageData)
      processUserInput({ mode, item, lotNo, data: userInputData });
  };

  return {
    state: {},
    action: { handleSaveUserInput },
  };
};

export default useSaveUserInput;
