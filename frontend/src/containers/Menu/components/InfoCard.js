import React from "react";
const InfoCard = ({ src, title, count }) => {
  return (
    <div className="flex-col items-center rounded-lg bg-white py-2">
      <div className="flex items-center justify-center">
        <img src={src} alt={src.split("//").pop()} />
      </div>
      <div className="flex justify-center pt-2">{title.toUpperCase()}</div>
      <div className="flex justify-center gap-1 py-1">
        {count}
        <span>pcs</span>
      </div>
    </div>
  );
};

export default InfoCard;
