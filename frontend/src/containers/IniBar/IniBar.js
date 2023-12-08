import React from "react";

import SettingsUpload from "./components/SettingsUpload";
import ChipTypeInput from "./components/ChipTypeInput";

const IniBar = () => {
  return (
    <div className="flex h-full w-full gap-3 rounded-lg bg-red-300">
      <SettingsUpload />
      <ChipTypeInput />
    </div>
  );
};

export default IniBar;
