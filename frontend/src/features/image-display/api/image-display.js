import { QUERY_KEYS } from "@/constants/api-keys";
import { useQuery } from "@tanstack/react-query";

export const useQueryImageData = () => {
  const { data: imageData } = useQuery({
    queryKey: [QUERY_KEYS.API_IMAGE_DATA],
  });
  return imageData;
};

export const useQueryColorData = () => {
  const { data: colorData } = useQuery({
    queryKey: [QUERY_KEYS.API_COLORS],
  });
  return colorData;
};
