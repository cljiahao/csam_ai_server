import { Label } from "@/components/ui/label";
import { useCanvasContext } from "@/contexts/context";
import useInfoCount from "./hooks/useInfoCount";
import { useInfoBarContext } from "../../contexts/infoBarContext";

const InfoBarDetails = ({ page }) => {
  const { marks } = useCanvasContext();
  const { infoDetails } = useInfoBarContext();
  const { data } = useInfoCount(page);

  const detailsInfo = {
    lotNo: infoDetails.lotNo || "N/A",
    plate: infoDetails.plate || "N/A",
    no_of_pieces: data?.result || "0",
  };

  const renderDetail = (label, value) => (
    <div className="hw-full flex items-center gap-2">
      <Label className="text-wrap font-semibold">{label}</Label>
      <Label className="ml-1">{value}</Label>
    </div>
  );

  const renderRealData = () => {
    const isCDC = page.toUpperCase() === "CDC";
    return (
      <div className="flex-center flex-col gap-2">
        <Label className="font-semibold">
          {isCDC ? "Real / Total:" : "Real / Pred:"}
        </Label>
        <Label>
          {
            marks.filter(
              ({ circle }) =>
                circle.name !== "default" && circle.name !== "zoom",
            ).length
          }{" "}
          / {detailsInfo.no_of_pieces}
        </Label>
      </div>
    );
  };

  return (
    <div className="hw-full grid grid-cols-3 gap-4 rounded-lg border border-gray-300 bg-gray-100 p-4">
      <div className="hw-full col-span-2 flex flex-col gap-3">
        {renderDetail("Lot No:", detailsInfo.lotNo)}
        {renderDetail("Plate No:", detailsInfo.plate)}
      </div>
      {renderRealData()}
    </div>
  );
};

export default InfoBarDetails;
