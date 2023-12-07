import React from "react";

const AddRows = ({ id, colors, fol_col, setFolders, type }) => {
  const folder = id in fol_col[type] ? fol_col[type][id].folder : "";
  const color = id in fol_col[type] ? fol_col[type][id].color : "";
  const updateFolder = (e) => {
    const newState = Object.assign({}, fol_col);
    if (!(e.target.id in newState[type])) newState[type][e.target.id] = {};
    newState[type][e.target.id]["folder"] = e.target.value;
    setFolders(newState);
  };

  const updateColor = (e) => {
    const newState = Object.assign({}, fol_col);
    if (!(e.target.id in newState[type])) {
      newState[type][e.target.id] = {};
      newState[type][e.target.id]["folder"] = "";
    }
    newState[type][e.target.id]["color"] = e.target.value;
    setFolders(newState);
  };

  return (
    <form className="flex w-full gap-10 py-1 2xl:py-3" key={id}>
      <input
        className="h-8 w-full rounded-md border-2 border-gray-300 pl-2 2xl:h-10 2xl:pl-3"
        type="text"
        placeholder="Folder Name"
        value={folder}
        id={id}
        onChange={updateFolder}
      />
      <div className="flex h-8 w-full items-center justify-between 2xl:h-10 2xl:w-[50%]">
        <label htmlFor="colors" className="text-sm">
          Dot Color
        </label>
        <select
          name="colors"
          className="h-8 rounded-md border-2 border-gray-300 pl-1 2xl:h-10 2xl:pl-3"
          key={id}
          id={id}
          value={color}
          onChange={updateColor}
        >
          <option value="Color">Color</option>
          {colors.map((col, i) => (
            <option value={col} key={i}>
              {col}
            </option>
          ))}
        </select>
      </div>
    </form>
  );
};

export default AddRows;
