import React from "react";

const Input = ({ className, text, onChange }) => {
  return (
    <label className={className}>
      {text}
      <input
        type="file"
        accept=".png, .jpg, .jpeg"
        onClick={(event) => {
          event.currentTarget.value = "";
        }}
        onChange={onChange}
        hidden
      />
    </label>
  );
};

export default Input;
