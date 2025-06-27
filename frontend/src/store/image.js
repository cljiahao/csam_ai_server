import { createRef } from "react";
import { create } from "zustand";

const initImageState = {
  imageRef: createRef(),
  error: "",
  image: null,
};

export const useImageStore = create((set) => ({
  ...initImageState,

  // Define Action
  resetError: () => set({ error: initImageState.error }),
  resetImage: () => set({ image: initImageState.image }),
  resetStore: () => set(initImageState),
  setError: (error) => set({ error }),
  setImage: (image) => set({ image }),
}));

export default useImageStore;
