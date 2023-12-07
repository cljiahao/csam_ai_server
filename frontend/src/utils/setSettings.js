import { API } from "../core/config";

const updateSettings = async (settings) => {
  const resp = await fetch(`${API}/Settings/set_settings`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(settings),
  });
  const json = await resp.json();
  return json;
};

export default updateSettings;
