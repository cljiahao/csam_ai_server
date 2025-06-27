import { useState } from "react";
import {
  useQueryImageData,
  useSaveUserMutation,
} from "@/features/info-bar/api/info-bar";
import useBaseStore from "@/store/base";
import useMarksStore from "@/store/marks";

const useSaveUserInput = () => {
  const [isSaved, setSaved] = useState(true);

  const updateError = useBaseStore((state) => state.updateError);
  const marks = useMarksStore((state) => state.marks);

  const imageData = useQueryImageData();
  const { mutateAsync: processUserInput } = useSaveUserMutation(updateError);

  const handleSaveUserInput = async ({ mode, item, lotNo }) => {
    const targetFileNames = new Map(
      marks.map((mark) => [mark.id, mark.marker.label]),
    );

    const userInputData = {
      ...imageData,
      file_data_batches: imageData?.file_data_batches
        .map((batch) => ({
          ...batch,
          defect_records: batch.defect_records.reduce((result, file) => {
            if (targetFileNames.has(file.id)) {
              result.push({
                ...file,
                defect_mode: targetFileNames.get(file.id),
              });
            }
            return result;
          }, []),
        }))
        .filter((batch) => batch.defect_records?.length > 0), // Remove batches with no files
    };
    if (imageData)
      processUserInput({ mode, item, lotNo, data: userInputData }).then(() =>
        setSaved(true),
      );
  };

  return {
    state: { isSaved },
    action: { setSaved, handleSaveUserInput },
  };
};

export default useSaveUserInput;
