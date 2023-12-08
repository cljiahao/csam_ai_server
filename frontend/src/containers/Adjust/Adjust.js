import React, { useEffect, useContext, useRef } from "react";

import { AppContext } from "../../contexts/context";
import Slider from "./components/Slider";
import InputBar from "./components/InputBar";
import batch_chip_img from "../../utils/batch_chip_img";

const Adjust = () => {
  const { settings, range, quantity, setQuantity } = useContext(AppContext);
  const batch_chip = useRef({
    batch: useRef(null),
    chip: useRef(null),
  });
  let prev_time = useRef(new Date());

  useEffect(() => {
    if ((new Date() - prev_time.current) / 1000 > 0.5) {
      const batch_qty = batch_chip_img(settings, range, batch_chip, "batch");
      const chip_qty = batch_chip_img(settings, range, batch_chip, "chip");
      quantity.match.batch = batch_qty === quantity.input.batch ? true : false;
      quantity.match.chip = chip_qty === quantity.input.chip ? true : false;
      setQuantity({
        ...quantity,
        output: { batch: batch_qty, chip: chip_qty },
      });
      prev_time.current = new Date();
    }
  }, [range, settings, quantity]);

  return (
    <div className="h-full w-full">
      <div className="flex h-full w-full flex-col px-3">
        {settings.chip_type in range &&
          Object.keys(range[settings.chip_type]).map((k) => {
            return (
              <div className="flex h-[50%] w-full gap-3 first:pb-3" key={k}>
                <div className="flex h-full w-[47%] flex-col justify-center overflow-scroll overflow-x-hidden overflow-y-hidden rounded-lg bg-red-300">
                  {settings.imgUrl ? (
                    <canvas
                      className="h-full w-full"
                      ref={batch_chip.current[k]}
                    />
                  ) : (
                    <div className="m-auto mx-10 h-5/6 rounded-xl border-4 border-dashed border-gray-400 bg-gray-100" />
                  )}
                </div>
                <div className="flex h-full w-[53%] flex-col text-sm">
                  <Slider type={k} />
                  <InputBar type={k} />
                </div>
              </div>
            );
          })}
      </div>
    </div>
  );
};

export default Adjust;
