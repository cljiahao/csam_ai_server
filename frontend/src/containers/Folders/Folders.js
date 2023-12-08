import React, { useState, useEffect } from "react";
import { IoMenu } from "react-icons/io5";
import Swal from "sweetalert2";
import "./Folders.css";

import Button from "../common/Button";
import AddRows from "./components/AddRows";
import ButtonCont from "./components/ButtonsCont";
import getFolders from "../../utils/getFolders";
import updateFolders from "../../utils/setFolders";

const Folders = ({ openMenu }) => {
  const [count, setCount] = useState(0);
  const [folders, setFolders] = useState({ old: {}, new: {} });
  const [colors, setColours] = useState([]);

  useEffect(() => {
    const setStates = async () => {
      const fol_dict = await getFolders();
      setColours(fol_dict.colors);
      const fol_col = folders;
      Object.keys(fol_dict.folders).map(
        (k, i) =>
          (fol_col["old"][i] = { folder: k, color: fol_dict.folders[k] }),
      );
      setFolders(fol_col);
    };
    setStates();
  }, [count]);

  const updateBackend = async () => {
    const newDict = Object.assign({}, folders.new, folders.old);
    const newFolders = Object.values(newDict)
      .filter((i) => i.folder !== "")
      .reduce((res = {}, value) => {
        res[value.folder] = value.color;
        return res;
      }, {});

    const alert = await updateFolders(newFolders);

    Swal.fire({
      title: alert.title,
      text: alert.text,
      icon: alert.icon,
      confirmButtonText: alert.confirmButtonText,
    });
    return;
  };

  return (
    <div className="h-full w-full 2xl:text-lg">
      <div className="flex h-[10%] w-full items-center justify-between rounded-lg px-2 text-center 2xl:h-[8%] 2xl:px-3">
        <IoMenu className="cursor-pointer" size="1.5rem" onClick={openMenu} />
        <Button
          className="flex h-10 w-32 cursor-pointer items-center justify-center rounded-lg border-2 border-gray-600 bg-gray-600 text-white duration-300 ease-in hover:bg-gray-300 hover:text-gray-600 2xl:ml-3 2xl:h-12 2xl:w-40 "
          text={"Update Folders"}
          onClick={updateBackend}
        />
      </div>
      <div>
        {Object.keys(folders["old"]).map((k) => (
          <AddRows
            id={k}
            key={k}
            colors={colors}
            fol_col={folders}
            setFolders={setFolders}
            type={"old"}
          />
        ))}
        {Array(count)
          .fill("")
          .map((k, i) => {
            const id = i + Object.keys(folders["old"]).length;
            return (
              <AddRows
                id={id}
                key={id}
                colors={colors}
                fol_col={folders}
                setFolders={setFolders}
                type={"new"}
              />
            );
          })}
      </div>
      <div className="flex h-[10%] w-full items-center justify-end gap-3 rounded-lg p-3 2xl:h-[8%] 2xl:gap-5 2xl:p-5">
        <ButtonCont
          count={count}
          setCount={setCount}
          folders={folders}
          setFolders={setFolders}
        />
      </div>
    </div>
  );
};

export default Folders;
