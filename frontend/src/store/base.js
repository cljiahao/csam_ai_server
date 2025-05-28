import { create } from "zustand";

const initBase = {
  error: "",
};

const useBaseStore = create((set) => ({
  ...initBase,

  //Define Actions
  resetError: () => set(initBase),
  updateError: (error) => set({ error }),
}));

export default useBaseStore;
