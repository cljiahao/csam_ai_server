import React from "react";
import { IconContext } from "react-icons";
import { IoMenu } from "react-icons/io5";
import ButtonsCont from "./ButtonsCont";
import UploadCont from "./UploadCont";
import DetailsCont from "./DetailsCont";

const NavBar = ({ button_info, detail_info, upload_info, openMenu }) => {
  return (
    <nav className="border-b-2 border-slate-400">
      <div className="flex-center h-20 w-full 2xl:h-28">
        <IconContext.Provider
          value={{
            className: "cursor-pointer 2xl:w-10 w-8 h-full mx-3",
          }}
        >
          <div onClick={openMenu}>
            <IoMenu />
          </div>
        </IconContext.Provider>
        {detail_info && <DetailsCont detail_info={detail_info} />}
        <div className={`flex-center h-full ${!detail_info && "w-full"}`}>
          {button_info && <ButtonsCont button_info={button_info} />}
          {upload_info && <UploadCont upload_info={upload_info} />}
        </div>
      </div>
    </nav>
  );
};

export default NavBar;
