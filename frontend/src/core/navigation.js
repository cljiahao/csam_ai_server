import { FaHome } from "react-icons/fa";
import { MdOutlineMoveToInbox } from "react-icons/md";
import { LiaNetworkWiredSolid } from "react-icons/lia";

// Information for different sections or pages with descriptions
const navigation_info = [
  {
    name: "Home",
    url: "/",
    title: "Home Page",
    description: "Home Page",
    icon: FaHome,
    component: "Home",
  },
  {
    name: "CDC",
    url: "/CDC",
    title: "CSAM Defects Collections",
    description:
      "Webpage to assist production in collecting Good, NG and Others chip images.",
    icon: MdOutlineMoveToInbox,
    component: "CsamDC",
  },
  {
    name: "CAI",
    url: "/CAI",
    title: "CSAM AI",
    description:
      "Webpage to assist production in predicting NG chip images for final judgement.",
    icon: LiaNetworkWiredSolid,
    component: "CsamAI",
  },
];

export { navigation_info };
