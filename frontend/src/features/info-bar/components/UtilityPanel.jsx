import { useState } from "react";

import NavSheet from "@/components/widgets/nav_sheet/NavSheet";
import ColorPick from "@/components/widgets/color_pick/ColorPick";
import { navigation_info } from "@/core/navigation";
import useColorUtility from "../hooks/useColorUtility";

const UtilityPanel = ({ item }) => {
  const [error, setError] = useState();

  const {
    state: { colorRef, isOpen },
    action: { handleNavSheetOpen },
  } = useColorUtility({ setError });

  return (
    <NavSheet
      nav_info={navigation_info}
      open={isOpen}
      onOpenChange={() => handleNavSheetOpen(item)}
    >
      <ColorPick ref={colorRef} item={item} />
    </NavSheet>
  );
};

export default UtilityPanel;
