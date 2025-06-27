import { create } from "zustand";

const initMarkerState = {
  marks: [],
};

export const useMarkerStore = create((set) => ({
  ...initMarkerState,

  // Define Actions
  resetMarks: () => set(initMarkerState),
  addMark: (file_name, marker) =>
    set((state) => ({ marks: [...state.marks, { file_name, marker }] })),
  updateMark: (file_name, new_marker) =>
    set((state) => {
      const file_index = state.marks.findIndex(
        (mark) => mark.file_name === file_name,
      );
      if (file_index !== -1) {
        const updatedMarksArray = [...state.marks];
        updatedMarksArray[file_index].marker = new_marker; // Replace the marks array
        return { marks: updatedMarksArray };
      } else {
        return state;
      }
    }),
  removeMark: (file_name) =>
    set((state) => ({
      marks: state.marks.filter((mark) => mark.file_name !== file_name),
    })),
}));
