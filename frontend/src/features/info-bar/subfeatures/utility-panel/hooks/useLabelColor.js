import { useRef } from "react";

import {
  useFetchColors,
  useQueryColorData,
  useSaveColors,
} from "@/features/info-bar/api/info-bar";
import useBaseStore from "@/store/base";

const useLabelColor = () => {
  const colorRef = useRef();
  const updateError = useBaseStore((state) => state.updateError);
  const { mutateAsync: fetchColors } = useFetchColors(updateError);
  const { mutateAsync: saveColors } = useSaveColors(updateError);

  const colorData = useQueryColorData() || [];

  return {
    state: { colorRef, colorData },
    action: { fetchColors, saveColors },
  };
};

export default useLabelColor;
