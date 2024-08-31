import { useRef, useState } from "react";

const defaultDisplay = {
  x: 0,
  y: 0,
  oldX: 0,
  oldY: 0,
  scale: 1,
  width: 0,
  height: 0,
  pan: false,
  move: false,
};

export function useDisplay() {
  const ref = useRef();
  const [display, setDisplay] = useState({ ...defaultDisplay });

  const getRefRect = (toUpdateDict) => {
    const rect = ref.current.getBoundingClientRect();
    return { ...toUpdateDict, height: rect.height, width: rect.width };
  };

  function resetZoom(e) {
    if (e && e.currentTarget !== e.target) return;
    const updateDisplay = getRefRect({ ...defaultDisplay });
    setDisplay(updateDisplay);
  }

  return {
    ref,
    display,
    setDisplay,
    getRefRect,
    resetZoom,
  };
}
