import React, { useContext } from "react";
import { AppContext } from "../../../../contexts/context";

const ChipMarker = ({ move, display, highlight }) => {
  const { array, focus } = useContext(AppContext);
  return (
    <svg
      style={{ position: "absolute" }}
      width={display.width}
      height={display.height}
    >
      {Object.keys(array.chips).map((key) => {
        return Object.keys(array.chips[key]).map((k) => {
          const { x, y, color, radius } = array.chips[key][k];
          const cx = (x * display.width) / focus.width;
          const cy = (y * display.height) / focus.height;
          return (
            <circle
              key={k}
              cx={cx}
              cy={cy}
              r={radius}
              stroke={color}
              strokeWidth="2"
              fillOpacity="0"
              onClick={() => {
                move && highlight(key, k);
              }}
            />
          );
        });
      })}
    </svg>
  );
};

export default ChipMarker;
