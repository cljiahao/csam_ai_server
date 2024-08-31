import {
  CanvasContext,
  DisplayContext,
  FolderHexContext,
  ImageDetailsContext,
} from "@/contexts/csamContext";
import { useDisplay } from "@/hooks/useDisplay";
import { useMarkCanvas } from "@/hooks/useMarkCanvas";
import { useFolderHex } from "@/hooks/useFolderHex";
import { useImageDetails } from "@/hooks/useImageDetails";

export const AppProvider = ({ children }) => {
  const statePanZoom = useDisplay();
  const stateImageDetails = useImageDetails();
  const stateMarkCanvas = useMarkCanvas();

  return (
    <DisplayContext.Provider value={statePanZoom}>
      <ImageDetailsContext.Provider value={stateImageDetails}>
        <CanvasContext.Provider value={stateMarkCanvas}>
          <FolderHexProvider>{children}</FolderHexProvider>
        </CanvasContext.Provider>
      </ImageDetailsContext.Provider>
    </DisplayContext.Provider>
  );
};

export const FolderHexProvider = ({ children }) => {
  const stateFolderHex = useFolderHex();
  return (
    <FolderHexContext.Provider value={stateFolderHex}>
      {children}
    </FolderHexContext.Provider>
  );
};
