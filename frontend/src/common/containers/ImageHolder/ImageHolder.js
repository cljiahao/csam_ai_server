import React, { useState, useEffect, useRef, useContext } from "react";
import { AppContext } from "../../../contexts/context";

import { initialDisplay } from "../../../core/config";
import ChipMarker from "./components/Canvas";

const ImageHolder = ({ highlight }) => {
  const { array, focus, setFocus, trigger } = useContext(AppContext);
  const [display, setDisplay] = useState(initialDisplay);
  const [mouse, setMouse] = useState({ pan: false, move: false });
  const containerRef = useRef();

  const mouse_delta = 10;

  useEffect(() => {
    if (focus.state === true) {
      const rect = containerRef.current.getBoundingClientRect();
      setDisplay((prevDisplay) => ({
        ...prevDisplay,
        x:
          (rect.width / 2 - (focus.x * rect.width) / focus.width) * focus.scale,
        y:
          (rect.height / 2 - (focus.y * rect.height) / focus.height) *
          focus.scale,
        scale: focus.scale,
      }));
    } else {
      setDisplay((prevDisplay) => ({
        ...prevDisplay,
        x: focus.x,
        y: focus.y,
        scale: focus.scale,
      }));
    }
  }, [focus]);

  useEffect(() => {
    const update_disp = () => {
      const rect = containerRef.current.getBoundingClientRect();
      setDisplay({ ...display, width: rect.width, height: rect.height });
    };
    window.addEventListener("resize", update_disp);
    return () => {
      window.removeEventListener("resize", update_disp);
    };
  });

  useEffect(() => {
    const onMouseUp = () => {
      setMouse({ ...mouse, pan: false });
    };
    const onMouseMove = (e) => {
      if (mouse.pan) {
        setDisplay({
          ...display,
          x: display.x + e.clientX - display.oldX,
          y: display.y + e.clientY - display.oldY,
          oldX: e.clientX,
          oldY: e.clientY,
        });
        const diffx = Math.abs(display.x + e.clientX - display.oldX);
        const diffy = Math.abs(display.y + e.clientY - display.oldY);
        if (mouse_delta < diffx && mouse_delta < diffy)
          setMouse({ ...mouse, move: false });
      }
    };

    window.addEventListener("mouseup", onMouseUp);
    window.addEventListener("mousemove", onMouseMove);
    return () => {
      window.removeEventListener("mouseup", onMouseUp);
      window.removeEventListener("mousemove", onMouseMove);
    };
  });

  const onMouseDown = (e) => {
    e.preventDefault();
    setMouse({ pan: true, move: true });
    setDisplay({
      ...display,
      oldX: e.clientX,
      oldY: e.clientY,
    });
  };

  const onWheel = (e) => {
    if (e.deltaY) {
      const sign = Math.sign(e.deltaY) / 10;
      const scale = 1 - sign;
      const rect = containerRef.current.getBoundingClientRect();
      if (display.scale >= 1) {
        setDisplay({
          ...display,
          x: display.x * scale - (rect.width / 2 - e.clientX + rect.x) * sign,
          y:
            display.y * scale -
            ((focus.height * rect.width) / focus.width / 2 -
              e.clientY +
              rect.y) *
              sign,
          scale: display.scale * scale,
          width: rect.width,
          height: rect.height,
        });
      } else setDisplay({ ...display, x: 0, y: 0, scale: 1 });
    }
  };

  const resetFocus = () => {
    setFocus({
      ...focus,
      state: false,
      x: 0,
      y: 0,
      scale: 1,
    });
  };

  const onLoad = (e) => {
    setFocus({
      ...focus,
      width: e.target.naturalWidth,
      height: e.target.naturalHeight,
    });
    const rect = containerRef.current.getBoundingClientRect();

    setDisplay({
      oldX: 0,
      oldY: 0,
      x: 0,
      y: 0,
      scale: 1,
      width: rect.width,
      height: rect.height,
    });
  };

  return (
    <div
      className="flex-center h-full w-full"
      ref={containerRef}
      onMouseDown={onMouseDown}
      onWheel={onWheel}
      onDoubleClick={resetFocus}
    >
      <div
        className="flex-center h-full w-full"
        style={{
          transform: `translate(${display.x}px, ${display.y}px) scale(${display.scale})`,
        }}
      >
        {array.chips && (
          <ChipMarker
            move={mouse.move}
            display={display}
            highlight={highlight}
          />
        )}
        <img
          src={trigger.image}
          alt={trigger.image}
          className="h-full w-full object-fill"
          onLoad={onLoad}
        />
      </div>
    </div>
  );
};

export default ImageHolder;
