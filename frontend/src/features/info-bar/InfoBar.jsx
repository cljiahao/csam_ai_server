import { useLocation } from "react-router-dom";

import InfoBarContext from "./contexts/InfoBarContext";
import useInfobar from "./hooks/useInfobar";
import UtilityPanel from "./subfeatures/utility-panel/UtilityPanel";
import MetricsPanel from "./components/MetricsPanel";
import UploadFormDialog from "./subfeatures/upload-form-dialog/UploadFormDialog";
import HoverButton from "@/components/widgets/hover-button/HoverButton";
import { navigation_info } from "@/core/navigation";

const InfoBar = () => {
  const location = useLocation();
  const mode = location.pathname.split("/").filter((path) => path !== "")[0];
  const nav = navigation_info.find((nav) => nav.name === mode);

  const { state: infoBarState, action: infoBarAction } = useInfobar();

  return (
    <InfoBarContext.Provider value={{ ...infoBarState, ...infoBarAction }}>
      <div className="flex-between h-20 w-full">
        <UtilityPanel />
        <MetricsPanel mode={mode} />
        <div className="px-2">
          <UploadFormDialog
            triggerChildren={
              <HoverButton
                // className={isSaved ? "" : "bg-red-300"}
                icon={nav.icon}
                hoverText={`${nav.name} Upload`}
              />
            }
            mode={mode}
          />
        </div>
      </div>
    </InfoBarContext.Provider>
  );
};

export default InfoBar;
