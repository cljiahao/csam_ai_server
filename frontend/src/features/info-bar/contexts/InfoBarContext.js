import { createContext, useContext } from "react";

const InfoBarContext = createContext(null);

export const useInfoBarContext = () => useContext(InfoBarContext);

export default InfoBarContext;
