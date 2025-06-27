import { createContext, useContext } from "react";

const ImageHolderContext = createContext(null);

export const useImageHolderContext = () => useContext(ImageHolderContext);

export default ImageHolderContext;
