import React, { useContext, useState } from "react";
import Swal from "sweetalert2";

import { AppContext } from "../../../contexts/context";
import Button from "../../common/Button";
import updateSettings from "../../../utils/setSettings";

const ChipTypeInput = () => {
  const { settings, setSettings, range, quantity } = useContext(AppContext);
  const [short, setShort] = useState(false);

  const update_set = async () => {
    let result = 0;
    Object.keys(quantity.input).forEach((key) => {
      if (
        quantity.input[key] !== quantity.output[key] ||
        quantity.input[key] === 0
      )
        result += 1;
    });
    if (result === 0) {
      const alert = await updateSettings(range);

      Swal.fire({
        title: alert.title,
        text: alert.text,
        icon: alert.icon,
        confirmButtonText: alert.confirmButtonText,
      });
    } else {
      Swal.fire({
        title: "Quantity don't match",
        text: "Please ensure quantity match the image quantity or input quantity is more than 0",
        icon: "error",
        confirmButtonText: "Confirm",
      });
    }
  };

  return (
    <div className="mr-5 grid h-full w-full grid-cols-7 gap-3 p-2">
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
          className="flex h-8 w-32 cursor-pointer items-center justify-center rounded-lg border-2 border-gray-600 bg-gray-600 hover:bg-gray-300 2xl:h-10 2xl:w-40 2xl:text-lg"
          text={"Update Settings"}
          onClick={update_set}
        />
      </div>
    </div>
  );
};

export default ChipTypeInput;
