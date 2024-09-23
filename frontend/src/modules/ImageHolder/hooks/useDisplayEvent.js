import { useEffect } from "react";
import { useDisplayContext } from "@/contexts/context";

const useDisplayEvent = () => {
  const { display, setDisplay, getRefRect, resetZoom } = useDisplayContext();

  function UpdateInitialDisplay() {
    useEffect(() => {
      resetZoom();
    }, []);
  }

  function UpdateResizeWindow() {
    useEffect(() => {
      const update_disp = () => {
        const updateDisplay = getRefRect({ ...display });
        setDisplay(updateDisplay);
      };
      window.addEventListener("resize", update_disp);
      return () => {
        window.removeEventListener("resize", update_disp);
      };
    });
  }

  return [UpdateInitialDisplay, UpdateResizeWindow];
};

export default useDisplayEvent;
