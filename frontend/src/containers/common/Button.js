import React from "react";

const Button = ({ but_class, span_class, onClick, icon, text }) => {
  return (
    <button className={but_class} onClick={onClick}>
      {icon}
      <span className={span_class}>{text}</span>
    </button>
  );
};

export default Button;
