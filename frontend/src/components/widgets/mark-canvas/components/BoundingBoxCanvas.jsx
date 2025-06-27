import useBoundingBoxMarker from "../hooks/useBoundingBoxMarker";

const BoundingBoxCanvas = ({ handleMark }) => {
  const {
    state: { generateRectangles },
  } = useBoundingBoxMarker();

  return (
    <>
      {generateRectangles.map((rectangle) => {
        return (
          <rect
            key={rectangle.id}
            id={rectangle.id}
            x={rectangle.x_start}
            y={rectangle.y_start}
            width={rectangle.width}
            height={rectangle.height}
            stroke={rectangle.color}
            strokeWidth={rectangle.thickness}
            fill="none"
            onClick={handleMark}
          />
        );
      })}
    </>
  );
};

export default BoundingBoxCanvas;
