import React from "react";

const Info = ({ data, info, type }) => {
  return (
    <ul className="flex w-full items-center gap-3 2xl:gap-6">
      <li className="info_list">
        <h1 className="info_head">Lot No:</h1>
        <div className="info_desc">{data.lot_no}</div>
      </li>
      <li className="info_list">
        <h1 className="info_head">Plate No:</h1>
        <div className="info_desc">{data.plate_no}</div>
      </li>
      {type === "CAI" ? (
        <li className="info_list">
          <h1 className="info_head">Predicted:</h1>
          <div className="info_desc">
            {info.no_of_pred_ng} <span className="info_unit">pcs</span>
          </div>
        </li>
      ) : null}
      <li className="info_list">
        <h1 className="info_head">Selected:</h1>
        <div className="info_desc">
          {Object.keys(info.no_of_real_ng).length === 0
            ? 0
            : Object.values(info.no_of_real_ng).reduce((a, b) => a + b, 0)}
          <span className="info_unit">pcs</span>
        </div>
      </li>
    </ul>
  );
};

export default Info;
