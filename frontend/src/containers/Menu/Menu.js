import React, { useContext } from "react";
import { IoMenu } from "react-icons/io5";
import { AppContext } from "../../contexts/context";
import "./Menu.css";

import NavBar from "./components/NavBar";
import InfoCardCont from "./components/InfoCardCont";
import Info from "../common/Info";

const Menu = ({ openMenu }) => {
  const { data, info, type } = useContext(AppContext);
  return (
    <div className="absolute left-0 top-0 h-screen w-full flex-col bg-gray-400">
      <nav className="flex h-[11%] w-full border-b-2 border-gray-300 2xl:h-[8%]">
        <div className="mx-1 flex h-full items-center justify-center 2xl:mx-2">
          <IoMenu className="cursor-pointer" size="1.5rem" onClick={openMenu} />
        </div>
        <NavBar />
      </nav>
      <section className="flex h-[15%] w-full items-center border-b-2 border-gray-300 p-5 2xl:h-[12%] 2xl:text-xl">
        <Info data={data} info={info} type={type} />
      </section>
      <section className="h-[74%] w-full py-3 2xl:h-[80%]">
        <InfoCardCont />
      </section>
    </div>
  );
};

export default Menu;
