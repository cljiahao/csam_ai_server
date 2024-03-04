import React, { useContext } from "react";
import { AppContext } from "../../contexts/context";

import BatchZones from "./components/BatchZones";

const Gallery = ({ highlight }) => {
  const { array } = useContext(AppContext);

  return (
    <div className="w-full overflow-y-auto border-l-2 border-gray-300 bg-gray-100">
      {array.chips && (
        <BatchZones highlight={highlight} batches={array.chips} />
      )}
    </div>
  );
};

export default Gallery;
