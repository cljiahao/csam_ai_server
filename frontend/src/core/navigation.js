import { FaHome } from "react-icons/fa";
import { MdOutlineMoveToInbox } from "react-icons/md";
import { LiaNetworkWiredSolid } from "react-icons/lia";

// Information for different sections or pages with descriptions
const navigation_info = [
  {
    name: "home",
    url: "/",
    title: "Home Page",
    description:
      "Webpage to assist production in collecting Good, NG and Others chip images.",
    icon: FaHome,
  },
  {
    name: "cdc",
    url: "/CDC",
    title: "CSAM Defects Collections",
    description:
      "Webpage to assist production in collecting Good, NG and Others chip images.",
    icon: MdOutlineMoveToInbox,
  },
  {
    name: "cai",
    url: "/CAI",
    title: "CSAM AI",
    description:
      "Webpage to assist production in predicting NG chip images for final judgement.",
    icon: LiaNetworkWiredSolid,
  },
];

export { navigation_info };
