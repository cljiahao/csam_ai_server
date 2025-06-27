import { createRef } from "react";
import { create } from "zustand";

const initMarks = {
  markRef: createRef(),
  marks: [],
};

export const useMarksStore = create((set) => ({
  ...initMarks,

  //Define Actions
  resetMarks: () => set(initMarks),
  setMarks: (marks) => set({ marks }),
}));

export default useMarksStore;
