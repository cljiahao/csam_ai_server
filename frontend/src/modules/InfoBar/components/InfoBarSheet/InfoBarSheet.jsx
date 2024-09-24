import NavModalSheet from "@/components/NavModalSheet/NavModalSheet";
import { useState } from "react";

const InfoBarSheet = () => {
  const [isOpen, setIsOpen] = useState(false);

  return <NavModalSheet open={isOpen} onOpenChange={setIsOpen}></NavModalSheet>;
};

export default InfoBarSheet;
