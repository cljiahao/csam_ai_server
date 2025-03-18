import { useEffect, useRef, useState } from "react";
import { useMutation, useQueryClient } from "@tanstack/react-query";

import { getDotColors, saveDotColors } from "@/services/dotColorsService";
import { useColorStore } from "@/store/color";

const useFetchColors = ({ setError }) => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationKey: ["fetchColors"],
    mutationFn: async ({ item }) => await getDotColors(item),
    onSuccess: (data) => {
      queryClient.setQueryData(["fetchedColors"], data);
    },
    onError: (error) => {
      console.log(error.message);
      setError(error.message);
      queryClient.removeQueries(["fetchedColors"]); // Clear cache on error
    },
  });
};

const useSaveColors = ({ setError }) => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationKey: ["saveColors"],
    mutationFn: async ({ itemDotColors }) => await saveDotColors(itemDotColors),
    onSuccess: (data) => {
      queryClient.setQueryData(["savedColors"], data);
    },
    onError: (error) => {
      console.log(error.message);
      setError(error.message);
      queryClient.removeQueries(["savedColors"]); // Clear cache on error
    },
  });
};

const useColorUtility = ({ setError }) => {
  const colorRef = useRef();

  const [isOpen, setIsOpen] = useState(false);

  const setZColors = useColorStore((state) => state.setColors);

  const { mutateAsync: fetchColors, data: colorData } = useFetchColors({
    setError,
  });
  const { mutateAsync: saveColors } = useSaveColors({ setError });

  function handleNavSheetOpen(item) {
    const dotColors = colorRef?.current?.colors;
    if (!isOpen) {
      fetchColors({ item });
    } else if (dotColors?.length > 0) {
      saveColors({ itemDotColors: { item: item, dot_colors_list: dotColors } });
      setZColors(dotColors);
    }
    setIsOpen(!isOpen);
  }

  useEffect(() => {
    const setColors = colorRef?.current?.setColors;
    if (setColors) {
      setColors(colorData?.dot_colors_list);
    }
  }, [colorData]);

  return {
    state: { colorRef, isOpen },
    action: { handleNavSheetOpen, fetchColors },
  };
};

export default useColorUtility;
