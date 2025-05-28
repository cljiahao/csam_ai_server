import { useLocation } from "react-router-dom";

import MetricsPanel from "./components/MetricsPanel";
import UploadFormDialog from "./subfeatures/upload-form-dialog/UploadFormDialog";
import UtilityPanel from "./subfeatures/utility-panel/UtilityPanel";

const InfoBar = () => {
  const location = useLocation();
  const mode = location.pathname.split("/").filter((path) => path !== "")[0];

  return (
    <div className="flex-between h-20 w-full flex-shrink-0 gap-3 px-3">
      <UtilityPanel />
      <MetricsPanel mode={mode} />
      <UploadFormDialog mode={mode} />
    </div>
  );
};

export default InfoBar;
