import React, { useEffect, useState } from "react";
import { Transition } from "@headlessui/react";
import "./CDC.css";
import {
  initialArray,
  initialData,
  initialFocus,
  initialInfo,
  initialState,
} from "../../core/config";

import { AppContext } from "../../contexts/context";
import { InfoBar, ImageHolder, Gallery } from "../../containers";
import saveData from "../../utils/saveData";
import changeColour from "../../utils/changeColour";
import Menu from "../../containers/Menu/Menu";

function CDC() {
  // Deep copy / clone initial states to prevent overlapping
  const [array, setArray] = useState(structuredClone(initialArray));
  const [data, setData] = useState(structuredClone(initialData));
  const [focus, setFocus] = useState(structuredClone(initialFocus));
  const [info, setInfo] = useState(structuredClone(initialInfo));
  const [state, setState] = useState(structuredClone(initialState));

  const type = "CDC";

  // useEffect(() => {
  //   const load = () => {
  //     save();
  //   };
  //   window.addEventListener("beforeunload", load);
  //   return () => {
  //     window.removeEventListener("beforeunload", load);
  //   };
  // }, [array]);

  const save = () => {
    const length =
      Object.keys(info.no_of_real_ng).length === 0
        ? 0
        : Object.values(info.no_of_real_ng).reduce((a, b) => a + b, 0);
    if (!state.error && data.lot_no && length > 0) saveData(array, data, info);
  };

  const highlight = (zone, key) => {
    const [array_dict, info_dict] = changeColour(zone, key, array, info, state);
    setArray({
      ...array,
      real_ng: array_dict.real_ng,
    });
    setInfo({
      ...info,
      no_of_real_ng: info_dict.no_of_real_ng,
    });
  };

  const openMenu = () => {
    setState({ ...state, menu: !state.menu });
  };

  return (
    <AppContext.Provider
      value={{
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
      }}
    >
      <div className="top-0 m-0 flex h-screen max-h-screen w-screen justify-between p-0">
        <main className="flex h-full max-h-screen w-[61%] 2xl:w-[65%]">
          <ImageHolder highlight={highlight} />
        </main>
        <aside className="relative flex h-full max-h-screen w-[39%] flex-col 2xl:w-[35%]">
          <InfoBar save={save} openMenu={openMenu} />
          <Gallery highlight={highlight} />
          <Transition
            show={state.menu}
            enter="transition-opacity ease-in duration-300"
            enterFrom="opacity-0"
            enterTo="opacity-100"
            leave="transition-opacity ease-in duration-300"
            leaveFrom="opacity-100"
            leaveTo="opacity-0"
          >
            <Menu openMenu={openMenu} />
          </Transition>
        </aside>
      </div>
    </AppContext.Provider>
  );
}

export default CDC;
