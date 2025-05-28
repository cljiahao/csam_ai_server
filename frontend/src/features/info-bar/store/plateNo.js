import { create } from "zustand";

const initPlateNoState = {
  plateNo: "",
};

export const usePlateNoStore = create((set) => ({
  ...initPlateNoState,

  // Define Action
  resetPlateNo: () => set(initPlateNoState),
  setPlateNo: (plateNo) => set({ plateNo }),
}));
