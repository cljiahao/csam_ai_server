import React from "react";

import Input from "../../components/Input";
import Button from "../../components/Button";

const ColorPick = ({ label, input_info, button_info }) => {
  return (
    <div className="flex-center w-full flex-col">
      <div className="flex-between h-14 w-full px-3">
        <div className="flex flex-col px-3 2xl:flex-row 2xl:gap-5 2xl:px-7">
          <span className="font-semibold underline">Item Type:</span> {label}
        </div>
        <Button button_info={button_info.add} />
      </div>
      {Object.keys(input_info).length > 0 && (
        <div className="flex-center w-full flex-col rounded-xl bg-slate-300 py-3">
          {Object.keys(input_info).map((key) => (
            <div key={key} className="flex-center h-16 w-full">
              <div className="h-full w-[80%]">
                <Input name={key} input_info={input_info[key]} />
              </div>
              <div className="flex-center w-[20%]">
                <Button name={key} button_info={button_info.remove} />
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default ColorPick;
