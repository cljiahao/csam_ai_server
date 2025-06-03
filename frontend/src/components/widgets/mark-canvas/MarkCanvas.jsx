import {
  cloneElement,
  forwardRef,
  isValidElement,
  useImperativeHandle,
} from "react";
import useMarkCanvas from "./hooks/useMarkCanvas";
import DotCanvas from "./components/DotCanvas";
import BoundingBoxCanvas from "./components/BoundingBoxCanvas";

const MarkCanvas = forwardRef(
  ({ children, imageSize, coordinates, canvasType = "dot" | "rect" }, ref) => {
    const markCanvasState = useMarkCanvas();
    const {
      state: { marks },
      action: { resetMarks, addMark, handleMark },
    } = markCanvasState;

    useImperativeHandle(ref, () => ({ resetMarks, addMark }));

    return (
      <svg
        className="absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2"
        width={imageSize?.width}
        height={imageSize?.height}
      >
        {canvasType.toLowerCase() == "dot" && (
          <DotCanvas
            imageSize={imageSize}
            marks={marks}
            coordinates={coordinates}
          />
        )}
        {canvasType.toLowerCase() == "rect" && (
          <BoundingBoxCanvas
            imageSize={imageSize}
            marks={marks}
            coordinates={coordinates}
          />
        )}
        {children && isValidElement(children)
          ? cloneElement(children, {
              imageSize,
              marks,
              handleMark,
            })
          : null}
      </svg>
    );
  },
);
MarkCanvas.displayName = "MarkCanvas";

export default MarkCanvas;
