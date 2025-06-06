import useDotMarker from "../hooks/useDotMarker";

const DotCanvas = ({ handleMark }) => {
  const {
    state: { generateCircles },
  } = useDotMarker();

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
            onClick={handleMark}
          />
        );
      })}
    </>
  );
};

export default DotCanvas;
