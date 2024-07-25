import React from "react";
import Input from "./Input";

const InputCont = ({ input_info }) => {
  return (
    <div className="flex-center h-full w-full gap-5 px-3">
      {Object.keys(input_info).map((key) => (
        <Input key={key} name={key} input_info={input_info[key]} />
      ))}
    </div>
  );
};

export default InputCont;
