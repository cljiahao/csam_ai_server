import { InfoBarProvider } from "./contexts/InfoBarProvider";
import InfoBarDetails from "./components/InfoBarDetails/InfoBarDetails";
import InfoBarUpload from "./components/InfoBarUpload/ImageForm";
import InfoBarSheet from "./components/InfoBarSheet/InfoBarSheet";

const InfoBar = ({ mode }) => {
  return (
    <InfoBarProvider>
      <div className="flex-between h-20 w-full flex-shrink-0 gap-3 px-3">
        <InfoBarSheet />
        <InfoBarDetails mode={mode} />
        <InfoBarUpload mode={mode} />
      </div>
    </InfoBarProvider>
  );
};

export default InfoBar;
