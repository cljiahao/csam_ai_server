import { useState } from "react";
import {
  useQueryImageData,
  useSaveUserMutation,
} from "@/features/info-bar/api/info-bar";
import useMarking from "@/hooks/useMarking";
import useBaseStore from "@/store/base";

const useSaveUserInput = () => {
  const [isSaved, setSaved] = useState(true);

  const updateError = useBaseStore((state) => state.updateError);
  const imageData = useQueryImageData();

  const {
    state: { marks },
  } = useMarking();

  const { mutateAsync: processUserInput } = useSaveUserMutation(updateError);

  const handleSaveUserInput = async ({ mode, item, lotNo }) => {
    const targetFileNames = new Map(
      marks.map((mark) => [mark.file_name, mark.marker.name]),
    );

    const userInputData = {
      ...imageData,
      file_data_batches: imageData?.file_data_batches
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
    if (imageData) processUserInput({ mode, item, lotNo, data: userInputData });
  };

  return {
    state: {},
    action: { handleSaveUserInput },
  };
};

export default useSaveUserInput;
