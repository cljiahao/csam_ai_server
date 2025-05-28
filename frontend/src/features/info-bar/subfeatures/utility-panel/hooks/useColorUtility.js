import { useEffect, useRef } from "react";
import { v4 as uuidv4 } from "uuid";

import { useColorStore } from "@/store/color";
import { useFetchColors, useSaveColors } from "../api/fetchColorUtility";
import useBaseStore from "@/store/base";

const useColorUtility = () => {
  const colorRef = useRef();
  const setZColors = useColorStore((state) => state.setColors);
  const updateError = useBaseStore((state) => state.updateError);

  const { mutateAsync: fetchColors, data: colorData } = useFetchColors({
    updateError,
  });
  const { mutateAsync: saveColors } = useSaveColors({ updateError });

  useEffect(() => {
    const setColors = colorRef?.current?.setColors;
    if (setColors) {
      const fetchedColors = colorData?.dot_colors_list || [];
      const colorsList =
        fetchedColors.length > 0
          ? fetchedColors
          : [{ uuid: uuidv4(), defect_label: "NG", hex_color: "#FFFF00" }];
      setColors(colorsList);
    }
  }, [colorData]);

  return {
    state: { colorRef },
    action: { saveColors, fetchColors, setZColors },
  };
};

export default useColorUtility;
