import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { getDotColors, saveDotColors } from "@/services/api-colors";
import { MUTATION_KEYS, QUERY_KEYS } from "@/constants/api-keys";
import { getAllModelHistory } from "@/services/api-ai-model";
import { getItemType } from "@/services/api-stats-data";
import { saveFinalJudgement, uploadImage } from "@/services/api-csam-image";

export const useLotNoMutation = (setError) => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationKey: [MUTATION_KEYS.API_ITEM],
    mutationFn: async (lotNo) => await getItemType(lotNo),
    onSuccess: (data) => {
      queryClient.setQueryData([QUERY_KEYS.API_ITEM], data);
    },
    onError: (error) => {
      setError(error);
      queryClient.removeQueries([QUERY_KEYS.API_ITEM]);
    },
  });
};

export const useImageDataMutation = (setError) => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationKey: [MUTATION_KEYS.API_IMAGE_DATA],
    mutationFn: async ({ mode, item, lotNo, formData }) =>
      await uploadImage(mode, item, lotNo, formData),
    onSuccess: (data) => {
      queryClient.setQueryData([QUERY_KEYS.API_IMAGE_DATA], data);
    },
    onError: (error) => {
      setError(error.message);
      queryClient.removeQueries([QUERY_KEYS.API_IMAGE_DATA]);
    },
  });
};

export const useSaveUserMutation = (setError) => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationKey: ["saveUserInput"],
    mutationFn: async ({ mode, item, lotNo, data }) =>
      await saveFinalJudgement(mode, item, lotNo, data),
    onSuccess: (data) => {
      queryClient.setQueryData(["saveUserInput"], data);
    },
    onError: (error) => {
      setError(error.message);
      queryClient.removeQueries(["saveUserInput"]); // Clear cache on error
    },
  });
};

export const useFetchColors = (setError) => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationKey: [MUTATION_KEYS.API_COLORS],
    mutationFn: async ({ item }) => await getDotColors(item),
    onSuccess: (data) => {
      queryClient.setQueryData([QUERY_KEYS.API_COLORS], data);
    },
    onError: (error) => {
      setError(error.message);
      queryClient.removeQueries([QUERY_KEYS.API_COLORS]);
    },
  });
};

export const useSaveColors = (setError) => {
  return useMutation({
    mutationFn: async ({ item, dotColors }) =>
      await saveDotColors(item, dotColors),
    onError: (error) => {
      setError(error.message);
    },
  });
};

export const useFetchModelHistory = (setError) => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationKey: [MUTATION_KEYS.modelHistory],
    mutationFn: async ({ item }) => await getAllModelHistory(item),
    onSuccess: (data, variables) => {
      queryClient.setQueryData([QUERY_KEYS.API_MODEL, variables.item], data);
    },
    onError: (error, variables) => {
      setError(error.message);
      queryClient.removeQueries([QUERY_KEYS.API_MODEL, variables.item]);
    },
  });
};

export const useQueryItem = () => {
  const { data: item } = useQuery({
    queryKey: [QUERY_KEYS.API_ITEM],
  });
  return item;
};

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

export const useQueryModelHistory = (item) => {
  const { data: modelHistory } = useQuery({
    queryKey: [QUERY_KEYS.API_MODEL, item],
  });
  return modelHistory;
};
