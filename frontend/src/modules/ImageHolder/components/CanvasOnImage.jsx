import { useMemo } from "react";
import {
  useCanvasContext,
  useDisplayContext,
  useImageDetailsContext,
} from "@/contexts/context";
import { usePanZoom } from "../hooks/usePanZoom";

const CanvasOnImage = () => {
  const { display, resetZoom } = useDisplayContext();
  const { marks, updateMarkSelected } = useCanvasContext();
  const { imageDetails } = useImageDetailsContext();
  const [onWheel, onPanning] = usePanZoom();

  const imageObj = useMemo(() => {
    if (imageDetails.image) {
      return URL.createObjectURL(imageDetails.image);
    }
    return "";
  }, [imageDetails.image]);


  return (
    // TODO: Add animation ease-out
    <div
      className="flex-center hw-full relative"
      onWheel={onWheel}
      onMouseDown={onPanning}
      onMouseUp={onPanning}
      onMouseMove={onPanning}
    >
      <div
        className="flex-center hw-full relative"
        style={{
          transform: `translate(${display.x}px, ${display.y}px) scale(${display.scale})`,
        }}
      >
        <svg className="hw-full absolute" onDoubleClick={resetZoom}>
          {marks?.map((info) => {
            const xc = info.norm_x * display.width;
            const yc = info.norm_y * display.height;
            return (
              <circle
                key={info.id}
                id={info.id}
                cx={xc}
                cy={yc}
                r={info.circle.radius}
                stroke={info.circle.color}
                strokeWidth="2"
                fillOpacity="0"
                onClick={(e) => !display.move && updateMarkSelected(e)}
              />
            );
          })}
        </svg>
        <img
          src={imageObj}
          alt={imageDetails.image.name}
          className="hw-full object-fill"
        />
      </div>
    </div>
  );
};

export default CanvasOnImage;
