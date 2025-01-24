import useMarking from "@/hooks/useMarking";
import { saveFinalJudgement } from "@/services/api_files";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";

const useSaveUserMutation = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationKey: ["saveUserInput"],
    mutationFn: async (data) => await saveFinalJudgement(data),
    onSuccess: (data) => {
      queryClient.setQueryData(["saveUserInput"], data);
    },
    onError: (error) => {
      console.log(error.message);
      queryClient.removeQueries(["saveUserInput"]); // Clear cache on error
    },
  });
};

const useSaveUserInput = () => {
  const { data: processImageData } = useQuery({
    queryKey: ["processedImageData"],
  });

  const {
    state: { marks },
  } = useMarking();

  const { mutate: processUserInput } = useSaveUserMutation();

  const handleSaveUserInput = () => {
    const targetFileNames = new Map(
      marks.map((mark) => [mark.file_name, mark.marker.name]),
    );

    const userInputData = {
      ...processImageData,
      defect_batches: processImageData?.defect_batches
        .map((batch) => ({
          ...batch,
          defect_files: batch.defect_files.reduce((result, file) => {
            if (targetFileNames.has(file.file_name)) {
              result.push({
                ...file,
                defect_mode: targetFileNames.get(file.file_name),
              });
            }
            return result;
          }, []),
        }))
        .filter((batch) => batch.defect_files.length > 0), // Remove batches with no files
    };

    if (processImageData) processUserInput(userInputData);
  };

  return {
    state: {},
    action: { handleSaveUserInput },
  };
};

export default useSaveUserInput;
