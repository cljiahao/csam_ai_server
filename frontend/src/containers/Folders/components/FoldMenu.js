import React from "react";
import { IoMenu } from "react-icons/io5";

import FoldNavBar from "./FoldNavBar";

const FoldMenu = ({ openMenu }) => {
  return (
    <div className="absolute left-0 top-0 h-screen w-full flex-col bg-gray-400">
      <nav className="flex h-full w-full p-3">
        <div className="flex h-[10%] items-center justify-center px-2 2xl:px-3">
          <IoMenu className="cursor-pointer" size="1.5rem" onClick={openMenu} />
        </div>
        <FoldNavBar />
      </nav>
    </div>
  );
};

export default FoldMenu;
