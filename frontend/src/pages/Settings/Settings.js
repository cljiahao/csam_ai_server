import React, { useState, useEffect } from "react";
import { Transition } from "@headlessui/react";
import { initialSettings } from "../../core/config";
import { AppContext } from "../../contexts/context";

import getSettings from "../../utils/getSettings";
import IniBar from "../../containers/IniBar/IniBar";
import Folders from "../../containers/Folders/Folders";
import Adjust from "../../containers/Adjust/Adjust";
import FoldMenu from "../../containers/Folders/components/FoldMenu";

function Settings() {
  const [range, setRange] = useState({});
  const [inText, setInText] = useState({});
  const [settings, setSettings] = useState(structuredClone(initialSettings));
  const [menu, setMenu] = useState(false);

  useEffect(() => {
    const setStates = async () => {
      const set_dict = await getSettings();
      setRange(set_dict);
      setInText(set_dict);
    };
    setStates();
  }, [settings.batchUrl, settings.chipUrl]);

  const openMenu = () => {
    setMenu(!menu);
  };

  return (
    <AppContext.Provider
      value={{
        settings,
        setSettings,
        menu,
        setMenu,
        range,
        setRange,
        inText,
        setInText,
      }}
    >
      <div className="max-w-screen flex h-screen max-h-screen w-screen overflow-hidden bg-sky-50">
        <section className="h-full w-[70%]">
          <div className="h-[18%] p-3 2xl:h-[15%]">
            <IniBar />
          </div>
          <div className="h-[82%] 2xl:h-[85%]">
            <Adjust />
          </div>
        </section>
        <aside className="relative h-full w-[30%] border-l-2 border-gray-300 bg-red-300 p-3">
          <Folders openMenu={openMenu} />
          <Transition
            show={menu}
            enter="transition-opacity ease-in duration-300"
            enterFrom="opacity-0"
            enterTo="opacity-100"
            leave="transition-opacity ease-in duration-300"
            leaveFrom="opacity-100"
            leaveTo="opacity-0"
          >
            <FoldMenu openMenu={openMenu} />
          </Transition>
        </aside>
      </div>
    </AppContext.Provider>
  );
}

export default Settings;
