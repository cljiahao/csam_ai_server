import { API } from "../core/config";

const iniSettings = async (chip_type) => {
  await fetch(`${API}/Settings/ini_settings`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ chip_type: chip_type }),
  });
};

export default iniSettings;
