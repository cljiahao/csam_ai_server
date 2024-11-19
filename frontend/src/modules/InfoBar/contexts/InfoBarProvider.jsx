import useInfoDetails from "../hooks/useInfoDetails";
import { InfoBarContext } from "./infoBarContext";

export const InfoBarProvider = ({ children }) => {
  const stateInfoDetails = useInfoDetails();

  return (
    <InfoBarContext.Provider value={stateInfoDetails}>
      {children}
    </InfoBarContext.Provider>
  );
};
