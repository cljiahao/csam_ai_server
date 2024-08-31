import { useContext, createContext } from "react";

const DisplayContext = createContext();
const useDisplayContext = () => useContext(DisplayContext);

const ImageDetailsContext = createContext();
const useImageDetailsContext = () => useContext(ImageDetailsContext);

const CanvasContext = createContext();
const useCanvasContext = () => useContext(CanvasContext);

const FolderHexContext = createContext();
const useFolderHexContext = () => useContext(FolderHexContext);

export {
  DisplayContext,
  useDisplayContext,
  ImageDetailsContext,
  useImageDetailsContext,
  CanvasContext,
  useCanvasContext,
  FolderHexContext,
  useFolderHexContext,
};
