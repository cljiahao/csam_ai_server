import { useState } from "react";
import NavModalSheet from "@/components/NavModalSheet/NavModalSheet";
import SettingsForm from "./components/SettingsForm";

const InfoBarSheet = ({ page }) => {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <NavModalSheet open={isOpen} onOpenChange={setIsOpen}>
      <SettingsForm page={page} />
    </NavModalSheet>
  );
};

export default InfoBarSheet;
