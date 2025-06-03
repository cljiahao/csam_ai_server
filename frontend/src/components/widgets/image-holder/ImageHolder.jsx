import { cn } from "@/lib/utils";
import {
  cloneElement,
  forwardRef,
  isValidElement,
  useImperativeHandle,
} from "react";

import PanAndZoom from "./components/PanAndZoom";
import Placeholder from "./components/PlaceHolder";
import ImageHolderContext from "./context/ImageHolderContext";
import { usePanZoom } from "./hooks/usePanZoom";
import useImageInfo from "./hooks/useImageInfo";

const ImageHolder = forwardRef(
  ({ className, children, image, placeholder_text }, ref) => {
    useImperativeHandle(ref, () => ({
      get moveActive() {
        return moveActive; // Always gets latest value
      },
      updateCoords,
      updateScale,
      resetCoords,
    }));

    const panZoomState = usePanZoom();
    const {
      state: { displayRef, moveActive },
      action: { updateCoords, updateScale, resetCoords },
    } = panZoomState;

    const imageState = useImageInfo();

    const {
      state: { imageSize },
    } = imageState;

    return (
      <ImageHolderContext.Provider value={{ image, panZoomState, imageState }}>
        <div
          className={cn("flex-center h-full w-full overflow-hidden", className)}
          ref={displayRef}
        >
          <Placeholder
            className={image ? "hidden" : ""}
            text={placeholder_text}
          />
          <PanAndZoom className={image ? "" : "hidden"}>
            {children && isValidElement(children)
              ? cloneElement(children, {
                  imageSize,
                })
              : null}
          </PanAndZoom>
        </div>
      </ImageHolderContext.Provider>
    );
  },
);
ImageHolder.displayName = "ImageHolder";

export default ImageHolder;
