import React, { useContext, useState } from "react";

import { AppContext } from "../../../contexts/context";
import Button from "../../common/Button";

const ChipTypeInput = () => {
  const [short, setShort] = useState(false);
  const { settings, setSettings, range } = useContext(AppContext);

  return (
    <div className="mr-5 grid h-full w-full grid-cols-7 gap-3 bg-red-300 p-2">
      <input
        className="col-span-5 rounded-md bg-gray-200 pl-3 text-gray-700"
        type="text"
        placeholder="Chip Type"
        onChange={(e) =>
          setSettings({ ...settings, chip_type: e.target.value })
        }
      />
      <label
        className="col-span-2 flex items-center gap-3 pl-2 text-sm 2xl:pl-5"
        htmlFor="short_form"
      >
        <input
          className="h-4 w-4 cursor-pointer 2xl:h-6 2xl:w-6"
          type="checkbox"
          id="short_form"
          checked={short}
          onChange={() => setShort(!short)}
        />
        Short Form
      </label>
      <div className="col-span-5 my-auto pl-3 text-gray-700">
        {short ? settings.chip_type.slice(0, 5) : null}
      </div>
      <div className="col-span-2 flex items-center pl-2 text-center text-base text-white hover:text-gray-600 2xl:pl-5">
        <Button
          className="flex h-8 w-32 cursor-pointer items-center justify-center rounded-lg border-2 border-gray-600 bg-gray-600 duration-300 ease-in hover:bg-gray-300 2xl:h-10 2xl:w-40 2xl:text-lg"
          text={"Update Settings"}
          onClick={() => setSettings(range)}
        />
      </div>
    </div>
  );
};

export default ChipTypeInput;
