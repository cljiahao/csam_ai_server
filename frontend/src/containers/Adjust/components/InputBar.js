import React, { useContext } from "react";
import { AppContext } from "../../../contexts/context";

import Button from "../../common/Button";
import getSettings from "../../../utils/getSettings";

const InputBar = ({ type }) => {
  const { settings, range, setRange, setInText } = useContext(AppContext);
  const chip_type = settings.chip_type;

  const setStates = async () => {
    const set_dict = await getSettings();
    setRange({
      ...range,
      [chip_type]: { ...range[chip_type], [type]: set_dict[chip_type][type] },
    });
    setInText({
      ...range,
      [chip_type]: { ...range[chip_type], [type]: set_dict[chip_type][type] },
    });
  };
  return (
    <div className="flex h-full w-full items-end justify-between px-3 pb-3 text-white">
      <Button
        className="h-10 w-16 cursor-pointer items-center justify-center rounded-lg border-2 border-gray-600 bg-gray-600 duration-300 ease-in hover:bg-gray-300 2xl:h-10 2xl:w-40 2xl:text-lg"
        text="reset"
        id={type}
        onClick={setStates}
      />
      <div className="flex items-center justify-center gap-3 text-black">
        <label>Quantity: </label>
        <input
          className="h-7 w-16 border-2 border-gray-500 text-center"
          type="text"
        />
        <div className="h-8 w-8 rounded-full bg-gray-500"></div>
      </div>
    </div>
  );
};

export default InputBar;
