import { create } from "zustand";

const initLotNoState = {
  lotNo: "",
};

export const useLotNoStore = create((set) => ({
  ...initLotNoState,

  // Define Action
  resetLotNo: () => set(initLotNoState),
  setLotNo: (lotNo) => set({ lotNo }),
}));
