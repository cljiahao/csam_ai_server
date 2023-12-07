import React, { useContext, useRef } from "react";
import Swal from "sweetalert2";

import cv from "@techstark/opencv-js";

import { AppContext } from "../../../contexts/context";
import Input from "../../common/Input";
import iniSettings from "../../../utils/iniSettings";

const SettingsUpload = () => {
  const { settings, setSettings } = useContext(AppContext);
  const imgRef = useRef(null);

  const sendData = async (e) => {
    if (settings.chip_type) {
      e.preventDefault();
      iniSettings(settings.chip_type);
      imgRef.current.src = URL.createObjectURL(e.target.files[0]);
      imgRef.current.onload = async () => {
        try {
          const img = cv.imread(imgRef.current);

          // For Batch image processing
          const batch_gray = new cv.Mat();
          cv.cvtColor(img, batch_gray, cv.COLOR_BGR2GRAY);

          // For Chips image processing
          const remove_bg = new cv.Mat();
          const blank = new cv.Mat(
            img.rows,
            img.cols,
            img.type(),
            [130, 130, 130, 255],
          );
          cv.compare(img, blank, remove_bg, cv.CMP_GT);
          img.setTo(new cv.Scalar.all(255), remove_bg);

          const chip_gray = new cv.Mat();
          cv.cvtColor(img, chip_gray, cv.COLOR_BGR2GRAY);

          setSettings({
            ...settings,
            batchUrl: batch_gray,
            chipUrl: chip_gray,
            file_name: e.target.files[0].name,
          });
        } catch (e) {
          console.log(e);
        }
      };
    } else {
      Swal.fire({
        title: "No Chip Type found",
        text: "Please key in the Chip Type you would like to process",
        icon: "error",
        confirmButtonText: "Confirm",
      });
    }
  };

  return (
    <div className="ml-5 flex w-[40%] items-center gap-3 break-all">
      <img className="hidden" alt="input" ref={imgRef} />
      <Input
        className="flex h-10 w-28 cursor-pointer items-center justify-center rounded-lg border-2 border-gray-600 bg-gray-600 text-center text-white duration-300 ease-in hover:bg-gray-300 hover:text-gray-600 2xl:ml-3 2xl:h-12 2xl:w-28 2xl:text-lg"
        text={"Upload"}
        onChange={sendData}
      />
      <div className="flex h-10 w-full items-center justify-center 2xl:text-xl">
        {settings.file_name}
      </div>
    </div>
  );
};

export default SettingsUpload;
