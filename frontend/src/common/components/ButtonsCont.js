import React from "react";
import Button from "./Button";

const ButtonsCont = ({ button_info }) => {
  return (
    <div className="flex-center h-full w-full gap-5 px-3">
      {Object.keys(button_info).map((key) => (
        <div key={key} className="h-full w-full">
          <Button name={key} button_info={button_info[key]} />
        </div>
      ))}
    </div>
  );
};

export default ButtonsCont;
