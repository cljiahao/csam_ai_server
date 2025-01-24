import { useCoordStores, useImageStore } from "./display";
import { useMarkerStore } from "./marker";

export const resetStore = () => {
  useCoordStores.getState().resetCoords();
  useImageStore.getState().resetImage();
  useMarkerStore.getState().resetMarks();
};
