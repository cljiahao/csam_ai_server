import { usePanZoom } from "../hooks/usePanZoom";

const PanAndZoom = ({ children, image }) => {
  const {
    state: { x, y, scale },
    action: { handlePan, onWheel, resetCoords },
  } = usePanZoom();

  function handleResetZoom(e) {
    if (e && e.target.tagName.toLowerCase() === "circle") return;
    resetCoords();
  }

  return (
    <div
      className="flex-center hw-full relative"
      onWheel={onWheel}
      onMouseDown={handlePan}
      onMouseUp={handlePan}
      onMouseMove={handlePan}
      onDoubleClick={handleResetZoom}
    >
      <div
        className="flex-center hw-full relative"
        style={{
          transform: `translate(${x}px, ${y}px) scale(${scale})`,
        }}
      >
        {children}
        <img src={image} alt="temp.jpg" className="hw-full object-fill" />
      </div>
    </div>
  );
};

export default PanAndZoom;
