import { Separator } from "@/components/ui/separator";
import NavSheet from "@/components/widgets/nav-sheet/NavSheet";
import { navigation_info } from "@/core/navigation";
import ModelHistory from "./components/ModelHistory";
import useUtilityPanel from "./hooks/useUtilityPanel";
import ColorPick from "../../../../components/widgets/color-pick/ColorPick";

const UtilityPanel = () => {
  const {
    state: { colorData, colorRef, isOpen, item },
    action: { handleNavSheetOpen },
  } = useUtilityPanel();

  return (
    <NavSheet
      nav_info={navigation_info}
      open={isOpen}
      onOpenChange={handleNavSheetOpen}
    >
      <div className="hw-full flex flex-col gap-2">
        <ModelHistory />
        <Separator className="h-[0.15em] rounded-xl bg-slate-300" />
        <ColorPick
          colorData={colorData}
          label="Item Type:"
          value={item}
          ref={colorRef}
        />
      </div>
    </NavSheet>
  );
};

export default UtilityPanel;
