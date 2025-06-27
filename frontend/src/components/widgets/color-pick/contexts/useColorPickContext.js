import { createContext, useContext } from "react";

const ColorPickContext = createContext(null);

export const useColorPickContext = () => useContext(ColorPickContext);

export default ColorPickContext;
