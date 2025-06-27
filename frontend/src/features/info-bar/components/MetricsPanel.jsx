import LabelValue from "@/components/static/label-value";
import { useMetrics } from "../hooks/useMetrics";

const MetricsPanel = ({ mode }) => {
  const {
    state: { lotNo, plateNo, count_ratio },
  } = useMetrics();

  return (
    <div className="hw-full grid grid-cols-3 gap-3 border border-gray-300 bg-gray-100 p-2">
      <div className="hw-full col-span-2 flex flex-col">
        <LabelValue label={"Lot No:"} value={lotNo} />
        <LabelValue label={"Plate No:"} value={plateNo} />
      </div>
      <LabelValue
        className="flex-center"
        label={`Real / ${mode === "CDC" ? "Total" : "Pred"}:`}
        value={`${count_ratio}`}
        toColumn
      />
    </div>
  );
};

export default MetricsPanel;
