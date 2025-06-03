import { cn } from "@/lib/utils";
import { useImageHolderContext } from "../context/ImageHolderContext";

const PanAndZoom = ({ className, children }) => {
  const { image, panZoomState, imageState } = useImageHolderContext();

  const {
    state: { x, y, scale },
    action: { handlePan, onWheel, resetCoords },
  } = panZoomState;

  const {
    state: { imageRef },
    action: { handleImageLoad },
  } = imageState;

  // TODO: remove static tagname circle and make it dynamic
  function handleResetZoom(e) {
    if (e && e.target.tagName.toLowerCase() === "circle") return;
    resetCoords();
  }

  return (
    <div
      className={cn("hw-full relative", className)}
      onWheel={onWheel}
      onMouseDown={handlePan}
      onMouseUp={handlePan}
      onMouseMove={handlePan}
      onDoubleClick={handleResetZoom}
    >
      <div
        className="hw-full relative"
        style={{
          transform: `translate(${x}px, ${y}px) scale(${scale})`,
        }}
      >
        {children}
        <img
          className="hw-full overflow-hidden object-contain"
          ref={imageRef}
          src={image}
          alt={image}
          onLoad={handleImageLoad}
        />
      </div>
    </div>
  );
};

export default PanAndZoom;
