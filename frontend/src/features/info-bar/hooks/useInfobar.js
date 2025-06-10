import { useState } from "react";
import useSaveUserInput from "./useSaveUserInput";

const useInfobar = () => {
  const [item, setItem] = useState("");
  const [lotNo, setLotNo] = useState("");
  const [plateNo, setPlateNo] = useState("");

  const {
    state: { isSaved },
    action: { setSaved, handleSaveUserInput },
  } = useSaveUserInput();

  return {
    state: { item, lotNo, plateNo, isSaved },
    action: { setItem, setLotNo, setPlateNo, setSaved, handleSaveUserInput },
  };
};

export default useInfobar;
