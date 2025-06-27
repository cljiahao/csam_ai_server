import { useState } from "react";

import { useInfoBarContext } from "@/features/info-bar/contexts/InfoBarContext";
import useModelHistory from "./useModelHistory";
import useLabelColor from "./useLabelColor";

const useUtilityPanel = () => {
  const [isOpen, setIsOpen] = useState(false);
  const { item } = useInfoBarContext();

  const {
    state: { colorRef, colorData },
    action: { fetchColors, saveColors },
  } = useLabelColor();

  const {
    action: { fetchModelHistory },
  } = useModelHistory();

  function handleNavSheetOpen() {
    if (!isOpen && item) {
      fetchColors({ item });
      fetchModelHistory({ item });
    } else if (colorRef?.current?.labelColors?.length > 0 && item) {
      saveColors({ item, dotColors: colorRef.current.labelColors });
    }
    setIsOpen(!isOpen);
  }
  return {
    state: { colorData, colorRef, isOpen, item },
    action: { handleNavSheetOpen },
  };
};

export default useUtilityPanel;
