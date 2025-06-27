import { create } from "zustand";

const initColorState = {
  colors: [], // Array of { label, value }
};

export const useColorStore = create((set) => ({
  ...initColorState,

  // Define Action
  resetColors: () => set(initColorState),
  setColors: (newColors) => set({ colors: newColors }),
}));
