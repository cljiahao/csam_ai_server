import HoverButton from "@/components/HoverButton";
import { useInfoBarContext } from "@/modules/InfoBar/contexts/infoBarContext";

const ImageFormButton = ({ form }) => {
  const { updateInfoDetails } = useInfoBarContext();

  function onReset() {
    form.reset();
    updateInfoDetails({ item: "" });
  }
  return (
    <div className="flex-between">
      <HoverButton type="submit">Upload</HoverButton>
      <HoverButton onClick={onReset}>Reset</HoverButton>
    </div>
  );
};

export default ImageFormButton;
