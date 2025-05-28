import { useQuery } from "@tanstack/react-query";
import useMarking from "@/hooks/useMarking";
import { usePlateNoStore } from "../store/plateNo";
import { useLotNoStore } from "../store/lotNo";

export const useMetrics = () => {
  const lotNo = useLotNoStore((state) => state.lotNo);
  const plateNo = usePlateNoStore((state) => state.plateNo);

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
    processImageData?.file_data_batches?.reduce((count, obj) => {
      return count + (obj.defect_records ? obj.defect_records.length : 0); // Add the length of `list`, handle undefined
    }, 0) ?? 0;

  const count_ratio = `${marks_count} / ${data_count}`;

  return { state: { lotNo, plateNo, count_ratio } };
};
