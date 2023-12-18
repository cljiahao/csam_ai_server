import React from "react";

import Button from "../../common/Button";

const ButtonCont = ({ count, setCount, folders, setFolders }) => {
  const deleteRow = () => {
    if (count > 0) {
      setCount(count - 1);
      const copyFolders = folders["new"];
      const keys = Object.keys(copyFolders);
      delete copyFolders[keys[keys.length - 1]];
      setFolders({ ...folders, new: copyFolders });
    } else {
      const copyFolders = folders["old"];
      const keys = Object.keys(copyFolders);
      delete copyFolders[keys[keys.length - 1]];
      setFolders({ ...folders, old: copyFolders });
    }
  };

  return (
    <>
      <Button
        but_class="flex h-10 w-10 items-center justify-center rounded-full bg-gray-600 text-xl font-bold 2xl:h-14 2xl:w-14"
        text={"+"}
        onClick={() => setCount(count + 1)}
      />
      <Button
        but_class="flex h-10 w-10 items-center justify-center rounded-full bg-gray-600 text-xl font-bold 2xl:h-14 2xl:w-14"
        text={"-"}
        onClick={deleteRow}
      />
    </>
  );
};

export default ButtonCont;
