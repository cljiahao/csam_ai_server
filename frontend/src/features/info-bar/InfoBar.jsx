import { useState } from "react";
import MetricsPanel from "./components/MetricsPanel";
import UploadFormDialog from "./components/UploadFormDialog";
import UtilityPanel from "./components/UtilityPanel";

const InfoBar = () => {
  const [item, setItem] = useState("");
  const [lotNo, setLotNo] = useState("");
  const [plateNo, setPlateNo] = useState("");

  return (
    <div className="flex-between h-20 w-full flex-shrink-0 gap-3 px-3">
      <UtilityPanel item={item} />
      <MetricsPanel lotNo={lotNo} plateNo={plateNo} />
      <UploadFormDialog
        item={item}
        setItem={setItem}
        lotNo={lotNo}
        setLotNo={setLotNo}
        setPlateNo={setPlateNo}
      />
    </div>
  );
};

export default InfoBar;
