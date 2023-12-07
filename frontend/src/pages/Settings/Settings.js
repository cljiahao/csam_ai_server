import React, { useState } from "react";
import { Transition } from "@headlessui/react";
import { initialSettings } from "../../core/config";
import { AppContext } from "../../contexts/context";

import IniBar from "../../containers/IniBar/IniBar";
import Folders from "../../containers/Folders/Folders";
import Adjust from "../../containers/Adjust/Adjust";
import FoldMenu from "../../containers/Folders/components/FoldMenu";

function Settings() {
  const [range, setRange] = useState({});
  const [settings, setSettings] = useState(structuredClone(initialSettings));
  const [menu, setMenu] = useState(false);

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
      }}
    >
      <div className="max-w-screen flex h-screen max-h-screen w-screen overflow-hidden">
        <section className="h-full w-[70%]">
          <div className="h-[18%] bg-purple-300 p-3 2xl:h-[15%]">
            <IniBar />
          </div>
          <div className="h-[82%] bg-pink-300 2xl:h-[85%]">
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
