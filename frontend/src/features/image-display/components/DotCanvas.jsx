import useMarkCanvas from "../hooks/useMarkCanvas";

const DotCanvas = ({ moveActive }) => {
  const {
    state: { circles },
    action: { onMark },
  } = useMarkCanvas();

  return (
    <svg className="hw-full absolute">
      {circles.map((circle) => (
        <circle
          key={circle.id}
          id={circle.id}
          cx={circle.cx}
          cy={circle.cy}
          r={circle.r}
          stroke={circle.color}
          strokeWidth="2"
          fillOpacity="0"
          onClick={(e) => !moveActive && onMark(e)}
        />
      ))}
    </svg>
  );
};

export default DotCanvas;
