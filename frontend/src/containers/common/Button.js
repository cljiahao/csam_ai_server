import React from "react";

const Button = ({ className, onClick, icon, text }) => {
  return (
    <button className={className} onClick={onClick}>
      {icon}
      {text}
    </button>
  );
};

export default Button;
