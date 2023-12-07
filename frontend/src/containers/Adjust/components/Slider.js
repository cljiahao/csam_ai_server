import React, { useContext } from "react";
import { AppContext } from "../../../contexts/context";

import Button from "../../common/Button";
import getSettings from "../../../utils/getSettings";

const Slider = ({ type }) => {
  const { settings, range, setRange } = useContext(AppContext);
  const chip_type = settings.chip_type;

  const rangeChange = (e) => {
    const value =
      e.target.value % 2 === 0
        ? parseInt(e.target.value)
        : parseInt(e.target.value) + 1;
    setRange({
      ...range,
      [chip_type]: {
        ...range[chip_type],
        [type]: { ...range[chip_type][type], [e.target.id]: value },
      },
    });
  };

  const setStates = async (e) => {
    const set_dict = await getSettings();
    setRange({
      ...range,
      [chip_type]: { ...range[chip_type], [type]: set_dict[chip_type][type] },
    });
  };

  return (
    <div className="h-[40%] w-full">
      <div className="w-full py-2">
        <label htmlFor="threshold">Threshold</label>
        <input
          className="w-full"
          type="range"
          id="threshold"
          min="1"
          max="255"
          value={range[chip_type][type].threshold}
          onChange={rangeChange}
        />
      </div>
      <div className="grid grid-cols-2 gap-x-2">
        {Object.keys(range[chip_type][type])
          .filter((k) => k !== "threshold")
          .map((key, i) => {
            return (
              <div key={i}>
                <label htmlFor={key}>{key}</label>
                <input
                  className="w-full"
                  id={key}
                  type="range"
                  min="1"
                  max="50"
                  value={range[chip_type][type][key]}
                  onChange={rangeChange}
                />
              </div>
            );
          })}
      </div>
      <div className="flex h-full w-full items-end justify-between px-3 pb-3 text-white">
        <Button
          className="h-10 w-16 cursor-pointer items-center justify-center rounded-lg border-2 border-gray-600 bg-gray-600 duration-300 ease-in hover:bg-gray-300 2xl:h-10 2xl:w-40 2xl:text-lg"
          text="reset"
          id={type}
          onClick={setStates}
        />
        <div className="flex items-center justify-center gap-3">
          <label className="text-black">Quantity: </label>
          <input className="h-7 w-16 border-2 border-gray-500" type="text" />
          <div className="h-8 w-8 rounded-full bg-gray-500"></div>
        </div>
      </div>
    </div>
  );
};

export default Slider;
