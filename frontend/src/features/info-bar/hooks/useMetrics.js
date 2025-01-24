import { useQuery } from "@tanstack/react-query";
import useMarking from "@/hooks/useMarking";

export const useMetrics = () => {
  const { data: processImageData } = useQuery({
    queryKey: ["processedImageData"],
  });

  const {
    state: { marks },
  } = useMarking();

  const marks_count = marks.filter(
    ({ marker }) => marker.name !== "default" && marker.name !== "zoom",
  ).length;
  const data_count =
    processImageData?.defect_batches?.reduce((count, obj) => {
      return count + (obj.defect_files ? obj.defect_files.length : 0); // Add the length of `list`, handle undefined
    }, 0) ?? 0;

  const count_ratio = `${marks_count} / ${data_count}`;

  return { state: { count_ratio } };
};
