import React from "react";

const DetailsCont = ({ detail_info }) => {
  return (
    <ul className="flex-between h-full w-full gap-2 pl-2 pr-5 text-center text-xs 2xl:text-lg">
      {Object.keys(detail_info).map((key) => (
        <li key={key} className="flex-center h-full flex-col gap-2 py-2">
          <h1 className="font-bold italic">{detail_info[key].name}</h1>
          <p className="flex-center h-full w-full">
            <span className="w-full">{detail_info[key].data}</span>
            {detail_info[key].unit && <span>{detail_info[key].unit}</span>}
          </p>
        </li>
      ))}
    </ul>
  );
};

export default DetailsCont;
