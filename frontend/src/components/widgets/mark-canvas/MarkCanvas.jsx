import { forwardRef, useImperativeHandle } from "react";
import useMarkCanvas from "./hooks/useMarkCanvas";
import DotCanvas from "./components/DotCanvas";
import BoundingBoxCanvas from "./components/BoundingBoxCanvas";
import MarkCanvasContext from "./context/MarkCanvasContext";

const MarkCanvas = forwardRef(
  (
    {
      imageSize,
      moveActive,
      canvasType,
      marks,
      setMarks,
      markColor,
      coordinates,
      showStatic = false,
    },
    ref,
  ) => {
    const {
      action: { resetMarks, addMark, removeMark, handleMark },
    } = useMarkCanvas(moveActive, marks, setMarks, markColor);

    useImperativeHandle(ref, () => ({
      resetMarks,
      addMark,
      removeMark,
      handleMark,
    }));

    if (moveActive) return; // To stop rendering the dots, improving speed.

    return (
      <MarkCanvasContext.Provider
        value={{ imageSize, marks, coordinates, showStatic }}
      >
        <svg
          className="absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2"
          width={imageSize?.width}
          height={imageSize?.height}
        >
          {canvasType.toLowerCase() == "dot" && (
            <DotCanvas handleMark={handleMark} />
          )}
          {canvasType.toLowerCase() == "rect" && (
            <BoundingBoxCanvas handleMark={handleMark} />
          )}
        </svg>
      </MarkCanvasContext.Provider>
    );
  },
);
MarkCanvas.displayName = "MarkCanvas";

export default MarkCanvas;
