import React from "react";
import MainCard from "./MainCard";
import { MdOutlineMoveToInbox } from "react-icons/md";
import { LiaNetworkWiredSolid } from "react-icons/lia";
import { IoMdSettings } from "react-icons/io";

const MainCardCont = () => {
  const card_info = {
    CDC: {
      title: "CSAM Data Collections",
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
    Settings: {
      title: "Settings",
      short: "Settings",
      description: "Configurations webpage for user to edit parameters.",
      src: <IoMdSettings />,
      link: "/Settings",
    },
  };
  return (
    <div className="flex h-full w-full gap-10 ">
      {Object.values(card_info).map((values, i) => {
        return (
          <MainCard
            key={values}
            src={values.src}
            title={values.title}
            short={values.short}
            description={values.description}
            link={values.link}
          />
        );
      })}
    </div>
  );
};

export default MainCardCont;
