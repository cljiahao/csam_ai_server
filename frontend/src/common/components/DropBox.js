import React from "react";

const DropBox = ({ folder_name, onChange, drop, selected }) => {
  return (
    <div className="flex-center h-12 w-full 2xl:h-14">
      <label className="w-[30%] text-center" htmlFor="folder">
        {`Choose ${folder_name}:`}
      </label>
      <div className="flex-center h-full flex-1 px-5 py-2">
        <select
          className="h-full w-full rounded-lg text-center"
          name={folder_name}
          onChange={onChange}
          value={selected}
        >
          <option value="">---</option>

          {drop.constructor === Object ? (
            <>
              {Object.keys(drop).map((key) => (
                <optgroup
                  key={key}
                  label={key[0].toUpperCase() + key.slice(1)}
                  className="text-left"
                >
                  {drop[key].map((value) => (
                    <option
                      key={value}
                      value={key + "/" + value}
                      className="text-center"
                    >
                      {value}
                    </option>
                  ))}
                </optgroup>
              ))}
            </>
          ) : (
            <>
              {drop.map((value) => (
                <option key={value} value={value}>
                  {value}
                </option>
              ))}
            </>
          )}
        </select>
      </div>
    </div>
  );
};

export default DropBox;
