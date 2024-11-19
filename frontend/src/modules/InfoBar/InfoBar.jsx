import { InfoBarProvider } from "./contexts/InfoBarProvider";
import { InfoBarDetails, InfoBarSheet, InfoBarUpload } from "./components";

const InfoBar = ({ page }) => {
  return (
    <InfoBarProvider>
      <div className="flex-between h-20 w-full flex-shrink-0 gap-3 px-3">
        <InfoBarSheet page={page} />
        <InfoBarDetails page={page} />
        <InfoBarUpload page={page} />
      </div>
    </InfoBarProvider>
  );
};

export default InfoBar;
