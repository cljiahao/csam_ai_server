import { useState } from "react";

const useInfobar = () => {
  const [item, setItem] = useState("");
  const [lotNo, setLotNo] = useState("");
  const [plateNo, setPlateNo] = useState("");

  return {
    state: { item, lotNo, plateNo },
    action: { setItem, setLotNo, setPlateNo },
  };
};

export default useInfobar;
