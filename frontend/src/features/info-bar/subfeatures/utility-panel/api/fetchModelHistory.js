import { getAllModelHistory } from "@/services/api_ai_model";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";

export const useFetchModelHistory = ({ updateError }) => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationKey: ["mutModelHistory"],
    mutationFn: async ({ item }) => await getAllModelHistory(item),
    onSuccess: (data, variables) => {
      queryClient.setQueryData(["modelHistory", variables.item], data);
    },
    onError: (error, variables) => {
      updateError(error.message);
      queryClient.removeQueries(["modelHistory", variables.item]);
    },
  });
};

export const useQueryModelHistory = (item) => {
  const { data: modelHistory } = useQuery({
    queryKey: ["modelHistory", item],
  });
  return modelHistory;
};
