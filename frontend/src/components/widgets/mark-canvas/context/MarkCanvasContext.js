import { createContext, useContext } from "react";

const MarkCanvasContext = createContext(null);

export const useMarkCanvasContext = () => useContext(MarkCanvasContext);

export default MarkCanvasContext;
