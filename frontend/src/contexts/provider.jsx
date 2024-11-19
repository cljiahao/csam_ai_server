import { HelmetProvider } from "react-helmet-async";
import {
  CanvasContext,
  DisplayContext,
  ImageDetailsContext,
} from "@/contexts/context";
import { useDisplay } from "@/hooks/useDisplay";
import { useMarkCanvas } from "@/hooks/useMarkCanvas";
import { useImageDetails } from "@/hooks/useImageDetails";

export const AppProvider = ({ children }) => {
  const statePanZoom = useDisplay();
  const stateMarkCanvas = useMarkCanvas();
  const stateImageDetails = useImageDetails();

  return (
    <HelmetProvider>
      <DisplayContext.Provider value={statePanZoom}>
        <CanvasContext.Provider value={stateMarkCanvas}>
          <ImageDetailsContext.Provider value={stateImageDetails}>
            {children}
          </ImageDetailsContext.Provider>
        </CanvasContext.Provider>
      </DisplayContext.Provider>
    </HelmetProvider>
  );
};
