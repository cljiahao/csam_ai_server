import { useState } from "react";
import useColorUtility from "./useColorUtility";
import useModelHistory from "./useModelHistory";
import { useItemStore } from "@/features/info-bar/store/item";

const useUtilityPanel = () => {
  const item = useItemStore((state) => state.item);
  const [isOpen, setIsOpen] = useState(false);

  const {
    state: { colorRef },
    action: { fetchColors, saveColors, setZColors },
  } = useColorUtility();

  const {
    action: { fetchModelHistory },
  } = useModelHistory();

  function handleNavSheetOpen() {
    const dotColors = colorRef?.current?.colors;
    if (!isOpen && item) {
      fetchColors({ item });
      fetchModelHistory({ item });
    } else if (dotColors?.length > 0) {
      saveColors({ itemDotColors: { item: item, dot_colors_list: dotColors } });
      setZColors(dotColors);
    }
    setIsOpen(!isOpen);
  }
  return {
    state: { isOpen, colorRef, item },
    action: { handleNavSheetOpen },
  };
};

export default useUtilityPanel;
