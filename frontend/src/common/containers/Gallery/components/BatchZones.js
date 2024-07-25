import React from "react";
import Thumbnails from "./Thumbnails";

const BatchZones = ({ batches, highlight }) => {
  return (
    <div className="flex h-full w-full flex-col">
      {Object.keys(batches).map((zone, index) => (
        <div key={index}>
          <div className="border-b-2 border-black px-2 py-2 text-lg font-bold">
            {"Batch " + zone}
          </div>
          {batches[zone] && <Thumbnails highlight={highlight} zone={zone} />}
        </div>
      ))}
    </div>
  );
};

export default BatchZones;
