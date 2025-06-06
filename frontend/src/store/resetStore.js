import useBaseStore from "./base";
import useImageStore from "./image";
import useMarksStore from "./marks";

export const resetStore = () => {
  useBaseStore.getState().resetError();
  useImageStore.getState().resetStore();
  useMarksStore.getState().resetStore();
};
