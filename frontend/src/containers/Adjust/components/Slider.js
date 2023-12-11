import React, { useContext } from "react";
import { AppContext } from "../../../contexts/context";

const Slider = ({ type }) => {
  const { settings, range, setRange, inText, setInText } =
    useContext(AppContext);
  const chip_type = settings.chip_type;

  const rangeChange = (e) => {
    const value = parseInt(e.target.value);
    setRange({
      ...range,
      [chip_type]: {
        ...range[chip_type],
        [type]: { ...range[chip_type][type], [e.target.id]: value },
      },
    });
    setInText({
      ...range,
      [chip_type]: {
        ...range[chip_type],
        [type]: { ...range[chip_type][type], [e.target.id]: value },
      },
    });
  };

  const inputChange = (e) => {
    const limit = e.target.id === "threshold" ? 255 : 50;
    const value =
      e.target.value === ""
        ? 0
        : parseInt(e.target.value) > limit
          ? limit
          : parseInt(e.target.value);
    setInText({
      ...range,
      [chip_type]: {
        ...range[chip_type],
        [type]: { ...range[chip_type][type], [e.target.id]: value },
      },
    });
  };

  return (
    <div className="flex h-full w-full flex-col rounded-lg bg-red-300 p-2 2xl:text-xl">
      <div className="flex h-full w-full flex-col">
        <label htmlFor="threshold">Threshold</label>
        <div className="flex gap-2">
          <input
            className="w-full"
            id="threshold"
            type="range"
            min="1"
            max="255"
            value={range[chip_type][type].threshold}
            onChange={rangeChange}
          />
          <input
            className="h-6 w-12 border-2 border-gray-500 text-center 2xl:h-8 2xl:w-16"
            id="threshold"
            type="text"
            value={inText[chip_type][type].threshold}
            onChange={inputChange}
            onKeyDown={(e) => {
              if (e.key === "Enter") rangeChange(e);
            }}
          />
        </div>
      </div>
      <div className="grid grid-cols-2 gap-x-2">
        {Object.keys(range[chip_type][type])
          .filter((k) => k !== "threshold")
          .map((key, i) => {
            return (
              <div className="flex flex-col" key={i}>
                <label htmlFor={key}>{key}</label>
                <div className="flex gap-2">
                  <input
                    className="w-full"
                    id={key}
                    type="range"
                    min="1"
                    max="50"
                    value={range[chip_type][type][key]}
                    onChange={rangeChange}
                  />
                  <input
                    className="h-6 w-12 border-2 border-gray-500 text-center 2xl:h-8 2xl:w-16"
                    id={key}
                    type="text"
                    value={inText[chip_type][type][key]}
                    onChange={inputChange}
                    onKeyDown={(e) => {
                      if (e.key === "Enter") rangeChange(e);
                    }}
                  />
                </div>
              </div>
            );
          })}
      </div>
    </div>
  );
};

export default Slider;
