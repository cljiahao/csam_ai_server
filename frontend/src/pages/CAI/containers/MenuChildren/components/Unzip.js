import React, { useState } from "react";
import { PiFileZipFill } from "react-icons/pi";
import { FaCheck } from "react-icons/fa";
import { unzip_files } from "../../../../../utils/api_data";

import UploadCont from "../../../../../common/components/UploadCont";

const Unzip = () => {
  const [zstatus, setZStatus] = useState({
    filename: "No file chosen",
    tick: "",
  });

  const process = async (e) => {
    e.preventDefault();
    const file = e.target.files[0];
    if (file) {
      const res = await unzip_files(file);
      setZStatus({
        tick: res.ok ? "bg-green-300" : "bg-red-300",
        filename: file.name,
      });
    }
  };

  const upload_info = {
    unzip: {
      name: "Unzip",
      type: "file",
      icon: <PiFileZipFill />,
      style: { font: "text-3xl" },
      onClick: (e) => {
        e.currentTarget.value = "";
      },
      onChange: process,
    },
  };
  return (
    <div className="flex-between h-full w-full gap-3 px-1 2xl:gap-5 2xl:px-3">
      <div className="flex-start h-14 w-52 2xl:h-16 2xl:w-56">
        <UploadCont upload_info={upload_info} />
      </div>
      <div className="break-all text-sm 2xl:text-xl 2xl:font-semibold">
        <div>{zstatus.filename}</div>
      </div>
      <div
        className={`flex-center rounded-full border-2 border-gray-500 p-1 2xl:p-3 ${zstatus.tick}`}
      >
        <FaCheck />
      </div>
    </div>
  );
};

export default Unzip;
