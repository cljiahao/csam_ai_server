import { useContext, createContext } from "react";

const InfoBarContext = createContext();
const useInfoBarContext = () => useContext(InfoBarContext);

export { InfoBarContext, useInfoBarContext };
