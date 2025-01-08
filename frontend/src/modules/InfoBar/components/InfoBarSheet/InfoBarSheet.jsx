import { useState } from "react";
import NavModalSheet from "@/components/NavModalSheet/NavModalSheet";

const InfoBarSheet = ({ page }) => {
  const [isOpen, setIsOpen] = useState(false);

  return <NavModalSheet open={isOpen} onOpenChange={setIsOpen}></NavModalSheet>;
};

export default InfoBarSheet;
