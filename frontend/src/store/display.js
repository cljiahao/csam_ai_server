import { create } from "zustand";

const initCoordState = {
  x: 0,
  y: 0,
  scale: 1,
  moveActive: false,
};

export const useCoordStores = create((set) => ({
  ...initCoordState,

  // Define Action
  resetCoords: () => set(initCoordState),
  updateCoords: (dx, dy) =>
    set({
      x: dx,
      y: dy,
    }),
  updateScale: (scale) => set({ scale }),
  isMove: (moveActive) => set({ moveActive }),
}));

const initImageState = {
  imageRef: null,
  image: null,
  error: "",
};

export const useImageStore = create((set) => ({
  ...initImageState,

  // Define Action
  resetImage: () => set(initImageState),
  setImageRef: (imageRef) => set({ imageRef }),
  setImage: (file) => set({ image: URL.createObjectURL(file) }),
  setError: (error) => set({ error }),
}));
