import React from "react";
import Upload from "./Upload";

const UploadCont = ({ upload_info }) => {
  return (
    <div className="flex-center h-full gap-5 px-3">
      {Object.keys(upload_info).map((key) => (
        <Upload key={key} name={key} upload_info={upload_info[key]} />
      ))}
    </div>
  );
};

export default UploadCont;
