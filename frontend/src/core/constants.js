import { FaHome } from "react-icons/fa";
import { MdOutlineMoveToInbox } from "react-icons/md";
import { LiaNetworkWiredSolid } from "react-icons/lia";

// Information for different sections or pages with descriptions
const home_info = [
  {
    name: "CDC",
    title: "CSAM Defects Collections",
    description:
      "Webpage to assist production in collecting Good, NG and Others chip images.",
    icon: MdOutlineMoveToInbox,
  },
  {
    name: "CAI",
    title: "CSAM AI",
    description:
      "Webpage to assist production in predicting NG chip images for final judgement.",
    icon: LiaNetworkWiredSolid,
  },
  // {
  //   name: "config",
  //   title: "Settings",
  //   description: "Settings page for adjusting configurations.",
  //   icon: IoMdSettings,
  // },
];

// Navigation links with URLs and icons
const nav_info = [
  { name: "home", url: "/", icon: FaHome },
  { name: "CDC", url: "/CDC", icon: MdOutlineMoveToInbox },
  { name: "CAI", url: "/CAI", icon: LiaNetworkWiredSolid },
  // { name: "config", url: "/config", icon: IoMdSettings },
];

// Hover button configurations with icons
const hover_button_info = [
  { name: "CDC", icon: MdOutlineMoveToInbox },
  { name: "CAI", icon: LiaNetworkWiredSolid },
];

export { home_info, nav_info, hover_button_info };
