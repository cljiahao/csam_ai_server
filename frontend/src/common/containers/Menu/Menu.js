import React from "react";
import { Transition } from "@headlessui/react";
import { FaHome } from "react-icons/fa";
import { MdOutlineMoveToInbox } from "react-icons/md";
import { LiaNetworkWiredSolid } from "react-icons/lia";

import NavBar from "../../components/NavBar";

const Menu = ({ openMenu, menu, children }) => {
  const nav_info = {
    Main: {
      name: "Main",
      icon: <FaHome />,
      style: { menu: true, font: "text-3xl" },
      onClick: () => (window.location.href = "/"),
    },
    CDC: {
      name: "CDC",
      icon: <MdOutlineMoveToInbox />,
      style: { menu: true, font: "text-3xl" },
      onClick: () => (window.location.href = "/CDC"),
    },
    CAI: {
      name: "CAI",
      icon: <LiaNetworkWiredSolid />,
      style: { menu: true, font: "text-3xl" },
      onClick: () => (window.location.href = "/CAI"),
    },
  };
  return (
    <Transition
      show={menu}
      enter="transition-opacity ease-in duration-300"
      enterFrom="opacity-0"
      enterTo="opacity-100"
      leave="transition-opacity ease-in duration-300"
      leaveFrom="opacity-100"
      leaveTo="opacity-0"
    >
      <div className="absolute left-0 top-0 flex h-screen w-full flex-col overflow-x-hidden bg-gray-500">
        <NavBar openMenu={openMenu} button_info={nav_info} />
        <div className="w-full">{children}</div>
      </div>
    </Transition>
  );
};

export default Menu;
