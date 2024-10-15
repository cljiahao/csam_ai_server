import React from "react";

const Input = ({ name, input_info }) => {
  return (
    <div className="flex-center h-full w-full">
      <div className="flex-center h-[75%] w-full">
        {input_info.name && (
          <label className="flex-center h-full w-[75%] text-center">
            {input_info.name[0].toUpperCase() + input_info.name.slice(1) + ":"}
          </label>
        )}
        {typeof input_info.in_name !== "undefined" && (
          <div className="flex-center h-[75%] w-[75%]">
            <input
              className="flex-center h-full w-[75%] text-center"
              type={input_info.in_type}
              name={"key_" + name}
              value={input_info.in_name}
              onChange={input_info.onChange}
              onBlur={input_info.onfocusout}
              disabled={input_info.disabled}
            ></input>
          </div>
        )}

        <div
          className={`flex-center h-full px-3 ${
            input_info.type === "checkbox"
              ? "w-[30%] py-4 2xl:py-3"
              : "w-full py-2"
          }`}
        >
          <input
            className={`h-full w-full rounded-lg text-center ${input_info.bg_color}`}
            type={input_info.type}
            name={name}
            value={input_info.default}
            onChange={input_info.onChange}
            onBlur={input_info.onfocusout}
            disabled={input_info.disabled}
          />
        </div>
      </div>
    </div>
  );
};

export default Input;
