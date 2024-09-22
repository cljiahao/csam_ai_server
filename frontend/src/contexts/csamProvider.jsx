import {
  CanvasContext,
  DisplayContext,
  ImageDetailsContext,
} from "@/contexts/csamContext";
import { useDisplay } from "@/hooks/useDisplay";
import { useMarkCanvas } from "@/hooks/useMarkCanvas";
import { useImageDetails } from "@/hooks/useImageDetails";

export const AppProvider = ({ children }) => {
  const statePanZoom = useDisplay();
  const stateImageDetails = useImageDetails();
  const stateMarkCanvas = useMarkCanvas();

  return (
    <DisplayContext.Provider value={statePanZoom}>
      <ImageDetailsContext.Provider value={stateImageDetails}>
        <CanvasContext.Provider value={stateMarkCanvas}>
          {children}
        </CanvasContext.Provider>
      </ImageDetailsContext.Provider>
    </DisplayContext.Provider>
  );
};
