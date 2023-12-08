import React, { useContext } from "react";
import { IoMenu } from "react-icons/io5";
import { AppContext } from "../../contexts/context";
import "./InfoBar.css";
import {
  API,
  initialArray,
  initialData,
  initialFocus,
  initialInfo,
  initialState,
} from "../../core/config";

import dataProcess from "../../utils/dataProcess";
import uploadImage from "../../utils/uploadImage";

import Info from "../common/Info";
import Input from "../common/Input";
import Button from "../common/Button";

const InfoBar = ({ save, insertDB, openMenu }) => {
  const {
    array,
    data,
    focus,
    info,
    state,
    setArray,
    setData,
    setFocus,
    setInfo,
    setState,
    type,
  } = useContext(AppContext);

  const initialize = () => {
    setArray(initialArray);
    setData(initialData);
    setFocus(initialFocus);
    setInfo(initialInfo);
    setState(initialState);
  };

  const errorHandling = async (res) => {
    if (res.status === 404) {
      setState({
        ...state,
        error: true,
        image: {
          src: "error/error_lot_no.png",
          alt: "Error_Lot_No.png",
        },
      });
      return false;
    } else if (res.status === 400) {
      setState({
        ...state,
        error: true,
        image: { src: "error/error.png", alt: "Error.png" },
      });
      return false;
    } else {
      const json = await res.json();
      return json;
    }
  };

  const process = async (e) => {
    e.preventDefault();
    if (type === "CAI") await insertDB(type);
    initialize();

    if (
      data.lot_no === "" ||
      data.lot_no === null ||
      (data.plate_no != null &&
        data.plate_no.slice(0, 3).toLowerCase() === "end") ||
      state.error
    ) {
      data.lot_no = prompt("Please Scan or Input Lot Number.");
    }

    const file = e.target.files[0];
    if (file) {
      setState({
        ...state,
        image: { src: "error/loading.gif", alt: "Loading.gif" },
      });
      const res = await uploadImage(file, data, type);
      if (res) {
        const json = await errorHandling(res);
        if (json) {
          const [array_dict, data_dict, focus_dict, info_dict, state_dict] =
            dataProcess(json, array, data, focus, info, state, type);
          setArray(array_dict);
          setData(data_dict);
          setFocus(focus_dict);
          setInfo(info_dict);
          state_dict.image = {
            src: `${API}${data_dict.directory.split("backend")[1]}/Original/${
              file.name
            }`,
            alt: file.name,
          };
          setState(state_dict);
        }
      }
    }
  };

  return (
    <div className="flex h-[11%] w-full gap-2 border-b-2 border-gray-300 bg-gray-100 2xl:h-[8%] 2xl:gap-6">
      <div className="mx-1 flex h-full items-center justify-center 2xl:mx-2">
        <IoMenu className="cursor-pointer" size="1.5rem" onClick={openMenu} />
      </div>
      <div className="flex w-full items-center text-xs 2xl:text-sm">
        <Info data={data} info={info} type={type} />
      </div>
      <div className="my-1 mr-3 flex h-12 w-fit items-center justify-between gap-3 2xl:my-2 2xl:mr-5 2xl:h-14 2xl:gap-2">
        <Input
          className="flex h-full w-20 cursor-pointer items-center justify-center rounded-lg border-2 border-gray-600 bg-gray-600 text-center text-base text-white hover:bg-gray-300 hover:text-gray-600 2xl:ml-3 2xl:w-28 2xl:text-lg"
          text={type + " Upload"}
          onChange={process}
        />
        {type === "CDC" ? (
          <Button
            className="flex h-full w-20 cursor-pointer items-center justify-center rounded-lg border-2 border-blue-500 bg-blue-500 text-center text-base text-white hover:bg-blue-300 hover:text-blue-600 2xl:ml-3 2xl:w-28 2xl:text-lg"
            text="Submit"
            onClick={save}
          />
        ) : null}
      </div>
    </div>
  );
};

export default InfoBar;
