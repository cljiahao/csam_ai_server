import React, { useContext } from "react";
import { AppContext } from "../../contexts/context";
import PanAndZoom from "./components/PanAndZoom";
import "./ImageHolder.css";

const ImageHolder = ({ highlight }) => {
  const { state } = useContext(AppContext);
  return (
    <div className="flex h-full w-full flex-col justify-center overflow-scroll overflow-x-hidden overflow-y-hidden">
      {state.image.src ? (
        <PanAndZoom highlight={highlight} />
      ) : (
        <div className="m-auto mx-10 h-5/6 rounded-xl border-4 border-dashed border-gray-400 bg-gray-100" />
      )}
    </div>
  );
};

export default ImageHolder;
