import React, { useContext, useEffect, useState } from "react";
import Swal from "sweetalert2";
import { AppContext } from "../../../../contexts/context";
import { FaMinus } from "react-icons/fa";
import { IoMdAdd } from "react-icons/io";

import ColorPick from "../../../../common/containers/ColorPick/ColorPick";
import { getFolColor } from "../../../../utils/api_images";
import Unzip from "./components/Unzip";

const MenuChildren = () => {
  const { array, setArray, details, setDetails } = useContext(AppContext);
  const [input, setInput] = useState({});

  useEffect(() => {
    const get_fol_col = async () => {
      if (details.item) {
        const fol_col = await getFolColor(details.item);
        setInput(
          Object.assign(
            {},
            ...Object.keys(fol_col).map((key, index) => ({
              [index]: { key: key, name: key, value: fol_col[key] },
            })),
          ),
        );
      }
    };
    get_fol_col();
  }, [details]);

  const changeColor = (e) => {
    const split = e.currentTarget.name.split("_");
    if (split[0] === "key") {
      setInput({
        ...input,
        [split[split.length - 1]]: {
          ...input[split[split.length - 1]],
          name: e.target.value,
        },
      });
    } else {
      setInput({
        ...input,
        [split[split.length - 1]]: {
          ...input[split[split.length - 1]],
          value: e.target.value,
        },
      });
    }
  };

  const setColor = () => {
    Object.keys(input).forEach((key) => {
      if (input[key].key !== input[key].name) {
        const { [input[key].key]: sel, ...sel_rest } = array.selected;
        sel_rest[input[key].name] = sel;
        array.selected = sel_rest;
        const { [input[key].key]: cnt, ...cnt_rest } = details.real_ng;
        cnt_rest[input[key].name] = cnt;
        details.real_ng = cnt_rest;
        input[key].key = input[key].name;
      }
      const { [input[key].key]: col, ...fol_rest } = array.folders;
      fol_rest[input[key].name] = input[key].value;
      array.folders = fol_rest;
    });
    setArray((prevArray) => ({
      ...prevArray,
      folders: array.folders,
      selected: array.selected,
    }));
    setDetails((prevDetails) => ({ ...prevDetails, real_ng: details.real_ng }));
  };

  const addColor = () => {
    setInput({
      ...input,
      [Object.keys(input).length]: {
        key: "default",
        name: "default",
        value: "#FFFF00",
      },
    });
    array.folders["default"] = "#FFFF00";
    array.selected["default"] = {};
    details.real_ng["default"] = 0;
    setArray((prevArray) => ({
      ...prevArray,
      folders: array.folders,
      selected: array.selected,
    }));
    setDetails((prevDetails) => ({ ...prevDetails, real_ng: details.real_ng }));
  };

  const removeColor = (e) => {
    const name = e.currentTarget.name;
    if (Object.keys(input).length > 1) {
      const { [name]: _, ...rest } = input;
      setInput(rest);
      const { [input[name].name]: col, ...fol_rest } = array.folders;
      const { [input[name].name]: sel, ...sel_rest } = array.selected;
      const { [input[name].name]: cnt, ...cnt_rest } = details.real_ng;
      setArray((prevArray) => ({
        ...prevArray,
        folders: fol_rest,
        selected: sel_rest,
      }));
      setDetails((prevDetails) => ({ ...prevDetails, real_ng: cnt_rest }));
    } else {
      Swal.fire({
        icon: "error",
        title: "Oops...",
        text: "Minimum 1 defect colour required. Can't remove",
      });
    }
  };

  const input_info = Object.assign(
    {},
    ...Object.keys(input).map((key) => ({
      [key]: {
        in_name: input[key].name,
        in_type: "text",
        type: "color",
        default: input[key].value,
        onChange: changeColor,
        onfocusout: setColor,
      },
    })),
  );

  const button_info = {
    remove: {
      name: "Minus",
      icon: <FaMinus />,
      style: { circle: "rounded-full", font: "text-sm" },
      onClick: removeColor,
    },
    add: {
      name: "Add",
      icon: <IoMdAdd />,
      style: { width: "w-24", font: "text-lg" },
      onClick: addColor,
    },
  };

  return (
    <div className="flex-center w-full flex-col bg-white py-3">
      <div className="flex-center w-[95%] rounded-lg bg-slate-300">
        <Unzip />
      </div>
      <div className="flex-center w-[95%] flex-col">
        <ColorPick
          label={details.item}
          input_info={input_info}
          button_info={button_info}
        />
      </div>
    </div>
  );
};

export default MenuChildren;
