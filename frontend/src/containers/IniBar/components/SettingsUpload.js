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

          // Split image, threshold for background only mask and return background as full white
          const channel = new cv.MatVector();
          cv.split(img, channel);
          let combine = new cv.Mat();
          for (let j = 0; j < channel.size() - 1; ++j) {
            const cn_thres = new cv.Mat();
            cv.threshold(channel.get(j), cn_thres, 100, 255, cv.THRESH_BINARY);
            if (j === 0) combine = cn_thres;
            cv.bitwise_and(combine, cn_thres, combine);
          }
          img.setTo(new cv.Scalar.all(255), combine);

          const gray = new cv.Mat();
          cv.cvtColor(img, gray, cv.COLOR_BGR2GRAY);

          setSettings({
            ...settings,
            imgUrl: gray,
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
        className="flex h-10 w-28 cursor-pointer items-center justify-center rounded-lg border-2 border-gray-600 bg-gray-600 text-center text-white hover:bg-gray-300 hover:text-gray-600 2xl:ml-3 2xl:h-12 2xl:w-28 2xl:text-lg"
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
