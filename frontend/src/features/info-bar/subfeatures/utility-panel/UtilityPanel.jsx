import { Separator } from "@/components/ui/separator";
import NavSheet from "@/components/widgets/nav-sheet/NavSheet";
import ColorPick from "@/components/widgets/color-pick/ColorPick";
import { navigation_info } from "@/core/navigation";
import ModelHistory from "./components/ModelHistory";
import useUtilityPanel from "./hooks/useUtilityPanel";

const UtilityPanel = () => {
  const {
    state: { isOpen, colorRef, item },
    action: { handleNavSheetOpen },
  } = useUtilityPanel();

  return (
    <NavSheet
      nav_info={navigation_info}
      open={isOpen}
      onOpenChange={() => handleNavSheetOpen()}
    >
      <div className="hw-full flex flex-col gap-2">
        <ModelHistory />
        <Separator className="h-[0.15em] rounded-xl bg-slate-300" />
        <ColorPick ref={colorRef} item={item} />
      </div>
    </NavSheet>
  );
};

export default UtilityPanel;
