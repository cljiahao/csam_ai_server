import { useMutation, useQueryClient } from "@tanstack/react-query";
import { getDotColors, saveDotColors } from "@/services/api_colors";

export const useFetchColors = ({ updateError }) => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationKey: ["fetchColors"],
    mutationFn: async ({ item }) => await getDotColors(item),
    onSuccess: (data) => {
      queryClient.setQueryData(["fetchedColors"], data);
    },
    onError: (error) => {
      console.log(error.message);
      updateError(error.message);
      queryClient.removeQueries(["fetchedColors"]);
    },
  });
};

export const useSaveColors = ({ updateError }) => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationKey: ["saveColors"],
    mutationFn: async ({ itemDotColors }) => await saveDotColors(itemDotColors),
    onSuccess: (data) => {
      queryClient.setQueryData(["savedColors"], data);
    },
    onError: (error) => {
      console.log(error.message);
      updateError(error.message);
      queryClient.removeQueries(["savedColors"]);
    },
  });
};
