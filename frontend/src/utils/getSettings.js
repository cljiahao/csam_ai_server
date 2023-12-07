import { API } from "../core/config";

const getSettings = async () => {
  const resp = await fetch(`${API}/Settings/get_settings`, {
    method: "GET",
    headers: {
      Accept: "application/json",
    },
  });
  const json = await resp.json();
  return json;
};

export default getSettings;
