import { useQueryImageData } from "../api/info-bar";
import { useInfoBarContext } from "../contexts/InfoBarContext";

export const useMetrics = () => {
  const { lotNo, plateNo } = useInfoBarContext();

  const imageData = useQueryImageData();

  // update marks usage
  const marks = [];

  const marks_count = marks.filter(
    ({ marker }) => marker.name !== "default" && marker.name !== "zoom",
  ).length;

  const data_count =
    imageData?.file_data_batches?.reduce((count, obj) => {
      return count + (obj.defect_records ? obj.defect_records.length : 0); // Add the length of `list`, handle undefined
    }, 0) ?? 0;

  const count_ratio = `${marks_count} / ${data_count}`;

  return { state: { lotNo, plateNo, count_ratio } };
};
