import React from "react";
import { MdOutlineMoveToInbox } from "react-icons/md";
import { LiaNetworkWiredSolid } from "react-icons/lia";

import MainNav from "./containers/MainNav/MainNav";

function Main() {
  const card_info = {
    CDC: {
      title: "CSAM Defects Collections",
      short: "CDC",
      description:
        "Website to assist production in collecting Good, NG and Others chip images.",
      src: <MdOutlineMoveToInbox />,
      link: "/CDC",
    },
    CAI: {
      title: "CSAM AI",
      short: "CAI",
      description:
        "Website to assist production in predicting NG chip images for final judgement.",
      src: <LiaNetworkWiredSolid />,
      link: "/CAI",
    },
  };
  return (
    <div className="flex-center h-screen w-screen bg-amber-50">
      <div className="flex-between mx-20 h-[90%] w-full">
        <MainNav card_info={card_info} />
      </div>
    </div>
  );
}

export default Main;
