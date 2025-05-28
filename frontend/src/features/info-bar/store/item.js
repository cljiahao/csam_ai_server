import { create } from "zustand";

const initItemState = {
  item: "",
};

export const useItemStore = create((set) => ({
  ...initItemState,

  // Define Action
  resetItem: () => set(initItemState),
  setItem: (item) => set({ item }),
}));
