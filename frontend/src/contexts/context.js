import { useContext, createContext } from "react";

const DisplayContext = createContext();
const useDisplayContext = () => useContext(DisplayContext);

const CanvasContext = createContext();
const useCanvasContext = () => useContext(CanvasContext);

const ImageDetailsContext = createContext();
const useImageDetailsContext = () => useContext(ImageDetailsContext);

export {
  DisplayContext,
  useDisplayContext,
  CanvasContext,
  useCanvasContext,
  ImageDetailsContext,
  useImageDetailsContext,
};
