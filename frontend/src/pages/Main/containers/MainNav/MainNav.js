import React from "react";
import MainCard from "./components/MainCard";

const MainNav = ({ card_info }) => {
  return (
    <div className="flex h-full w-full gap-20">
      {Object.keys(card_info).map((key) => {
        return <MainCard key={key} card_info={card_info[key]} />;
      })}
    </div>
  );
};

export default MainNav;
