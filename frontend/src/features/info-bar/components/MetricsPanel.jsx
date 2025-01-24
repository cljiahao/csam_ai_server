import { useLocation } from "react-router-dom";

import LabelValue from "@/components/widgets/label_value/LabelValue";
import { useMetrics } from "../hooks/useMetrics";

const MetricsPanel = ({lotNo, plateNo}) => {
  const location = useLocation();
  const mode = location.pathname.split("/").pop();

  const {
    state: { count_ratio },
  } = useMetrics();

  return (
    <div className="hw-full grid grid-cols-3 gap-3 border border-gray-300 bg-gray-100 p-2">
      <div className="hw-full col-span-2 flex flex-col">
        <LabelValue label={"Lot No:"} value={lotNo} />
        <LabelValue label={"Plate No:"} value={plateNo} />
      </div>
      <div className="hw-full">
        <LabelValue
          label={`Real / ${mode === "CDC" ? "Total" : "Pred"}`}
          value={`${count_ratio}`}
          to_column
        />
      </div>
    </div>
  );
};

export default MetricsPanel;
