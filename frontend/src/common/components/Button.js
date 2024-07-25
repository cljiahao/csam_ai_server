import React from "react";

const Button = ({ name, button_info }) => {
  const font_info = {
    "text-4xl": {
      button: "text-4xl hover:text-3xl 2xl:text-5xl 2xl:hover:text-4xl",
      span: "text-3xl 2xl:4xl",
    },
    "text-3xl": {
      button: "text-3xl hover:text-2xl 2xl:text-4xl 2xl:hover:text-3xl",
      span: "text-2xl 2xl:3xl",
    },
    "text-2xl": {
      button: "text-2xl hover:text-xl 2xl:text-3xl 2xl:hover:text-2xl",
      span: "text-xl 2xl:2xl",
    },
    "text-xl": {
      button: "text-xl hover:text-lg 2xl:text-2xl 2xl:hover:text-xl",
      span: "text-lg 2xl:xl",
    },
    "text-lg": {
      button: "text-lg hover:text-base 2xl:text-xl 2xl:hover:text-lg",
      span: "text-base 2xl:lg",
    },
    default: {
      button: "text-base hover:text-xl 2xl:text-xl 2xl:hover:text-lg",
      span: "text-sm 2xl:base",
    },
    "text-sm": {
      button: "text-sm hover:text-lg 2xl:text-lg 2xl:hover:text-base",
      span: "text-xs 2xl:sm",
    },
  };

  const font = button_info.style?.font
    ? font_info[button_info.style?.font]
    : font_info["default"];
  const circle = button_info.style?.circle || "rounded-lg";

  return (
    <div className="flex-center h-full font-semibold">
      <button
        className={`flex-center group h-[75%] gap-2 p-3 hover:text-white disabled:cursor-not-allowed disabled:bg-red-300 
        ${font.button} ${button_info.style?.menu ? "" : "bg-blue-400 hover:bg-blue-600"} ${circle} ${button_info.style?.width}`}
        name={name}
        disabled={button_info.disabled}
        onClick={button_info.onClick}
      >
        {button_info?.icon}
        <span className={`hidden group-hover:block ${font.span}`}>
          {button_info.name}
        </span>
      </button>
    </div>
  );
};

export default Button;
