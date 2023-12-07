import React from "react";
import { MdOutlineMoveToInbox } from "react-icons/md";
import { LiaNetworkWiredSolid } from "react-icons/lia";
import { IoMdSettings } from "react-icons/io";
import { FaHome } from "react-icons/fa";
import { Outlet, Link } from "react-router-dom";

const FoldNavBar = () => {
  const nav_info = {
    Main: {
      link: "/",
      icon: <FaHome />,
    },
    CDC: {
      link: "/CDC",
      icon: <LiaNetworkWiredSolid />,
    },
    CAI: {
      link: "/CAI",
      icon: <MdOutlineMoveToInbox />,
    },
    Settings: {
      link: "/Settings",
      icon: <IoMdSettings />,
    },
  };

  return (
    <nav className="flex h-full w-full justify-center">
      <ul className="h-full w-full flex-col">
        {Object.keys(nav_info).map((key, i) => {
          return (
            <li
              className="flex h-[10%] w-full items-center py-9 pl-16 font-bold tracking-wider"
              key={key}
            >
              <Link
                to={nav_info[key].link}
                className="flex items-center justify-center gap-7 text-3xl hover:text-4xl 2xl:gap-9 2xl:text-4xl 2xl:hover:text-5xl"
                onClick={() => {
                  window.location.href = nav_info[key].link;
                }}
              >
                {nav_info[key].icon}
                {key}
              </Link>
            </li>
          );
        })}
      </ul>
      <Outlet />
    </nav>
  );
};

export default FoldNavBar;
