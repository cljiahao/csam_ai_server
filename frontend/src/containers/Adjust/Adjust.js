import React, { useEffect, useContext, useRef } from "react";

import { AppContext } from "../../contexts/context";
import Slider from "./components/Slider";
import getSettings from "../../utils/getSettings";
import batch_chip_img from "../../utils/batch_chip_img";

const Adjust = () => {
  const { settings, range, setRange } = useContext(AppContext);
  const batch_chip = useRef({
    batch: useRef(null),
    chip: useRef(null),
  });

  useEffect(() => {
    const setStates = async () => {
      const set_dict = await getSettings();
      setRange(set_dict);
    };
    setStates();
  }, [settings.batchUrl, settings.chipUrl]);

  useEffect(() => {
    batch_chip_img(settings, range, batch_chip, "batch");
    batch_chip_img(settings, range, batch_chip, "chip");
  }, [range, settings]);

  return (
    <div className="h-full w-full">
      <div className="h-full w-full flex-col bg-teal-200">
        {settings.chip_type in range &&
          Object.keys(range[settings.chip_type]).map((k) => {
            return (
              <div className="flex h-[50%] w-full" key={k}>
                <div className="flex h-full w-[50%] flex-col justify-center overflow-scroll overflow-x-hidden overflow-y-hidden bg-rose-400">
                  {settings.batchUrl || settings.chipUrl ? (
                    <canvas
                      className="h-full w-full"
                      ref={batch_chip.current[k]}
                    />
                  ) : (
                    <div className="m-auto mx-10 h-5/6 rounded-xl border-4 border-dashed border-gray-400 bg-gray-100" />
                  )}
                </div>
                <div className="h-full w-[50%] bg-yellow-300 px-3 text-sm">
                  <Slider type={k} />
                </div>
              </div>
            );
          })}
      </div>
    </div>
  );
};

export default Adjust;
