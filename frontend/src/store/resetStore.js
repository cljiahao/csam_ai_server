import { useColorStore } from "./color";
import { useCoordStores, useImageStore } from "./display";
import { useMarkerStore } from "./marker";

export const resetStore = () => {
  useColorStore.getState().resetColors();
  useCoordStores.getState().resetCoords();
  useImageStore.getState().resetImage();
  useMarkerStore.getState().resetMarks();
};
