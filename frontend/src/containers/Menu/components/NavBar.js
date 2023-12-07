import React from "react";
import { MdOutlineMoveToInbox } from "react-icons/md";
import { LiaNetworkWiredSolid } from "react-icons/lia";
import { IoMdSettings } from "react-icons/io";
import { FaHome } from "react-icons/fa";
import { Outlet, Link } from "react-router-dom";

const NavBar = () => {
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
    <nav className="mx-3 flex h-full w-full justify-center 2xl:mx-5">
      <ul className="flex items-center gap-7 2xl:gap-14">
        {Object.keys(nav_info).map((key, i) => {
          return (
            <li className="info_list" key={key}>
              <Link
                to={nav_info[key].link}
                className="flex items-center gap-1 text-xl font-bold not-italic tracking-wider hover:text-2xl 2xl:gap-2 2xl:text-2xl 2xl:hover:text-3xl"
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

export default NavBar;
