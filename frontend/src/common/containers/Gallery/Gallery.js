import React, { useContext } from "react";
import { AppContext } from "../../../contexts/context";

import BatchZones from "./components/BatchZones";

const Gallery = ({ highlight }) => {
  const { array } = useContext(AppContext);

  return (
    <div className="flex h-full w-full overflow-y-auto bg-gray-100">
      {array.chips && (
        <BatchZones batches={array.chips} highlight={highlight} />
      )}
    </div>
  );
};

export default Gallery;
