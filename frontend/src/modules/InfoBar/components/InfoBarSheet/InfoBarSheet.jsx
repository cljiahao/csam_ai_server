import {
  useCanvasContext,
  useFolderHexContext,
  useImageDetailsContext,
} from "@/contexts/csamContext";
import { Label } from "@/components/ui/label";
import NavModalSheet from "@/components/NavModalSheet/NavModalSheet";
import ColorPick from "@/components/ColorPick/ColorPick";
import { useInfoBarContext } from "../../contexts/infoBarContext";

const InfoBarSheet = () => {
  const { isLoading, folderHex, refreshFolderHex, updateFolderHex } =
    useFolderHexContext();
  const { updateMarks } = useCanvasContext();
  const { imageDetails } = useImageDetailsContext();
  const { infoDetails } = useInfoBarContext();

  function refreshFolderMark() {
    updateFolderHex();
    if (imageDetails.chips) {
      const colorSet = folderHex?.find(({ item }) => item === infoDetails.item);
      updateMarks(colorSet, imageDetails.chips);
    }
  }

  return (
    <NavModalSheet
      bool_function={(isOpen) =>
        isOpen ? refreshFolderHex() : refreshFolderMark()
      }
    >
      {!isLoading && (
        <ColorPick itemType={infoDetails.item}>
          <header className="hw-full flex-center gap-3">
            <Label className="flex-center h-full w-8">Item Type</Label>
            <Label className="flex-center hw-full text-wrap font-semibold">
              {infoDetails.item}
            </Label>
          </header>
        </ColorPick>
      )}
    </NavModalSheet>
  );
};

export default InfoBarSheet;
