import useDotMarker from "../hooks/useDotMarker";

const DotCanvas = ({ imageSize, marks, coordinates = [] }) => {
  const {
    state: { generateCircles },
  } = useDotMarker(imageSize, marks, coordinates);

  return (
    <>
      {generateCircles.map((circle) => {
        return (
          <circle
            key={circle.id}
            id={circle.id}
            cx={circle.cx}
            cy={circle.cy}
            r={circle.r}
            stroke={circle.color}
            strokeWidth="2"
            fillOpacity="0"
          />
        );
      })}
    </>
  );
};

export default DotCanvas;
