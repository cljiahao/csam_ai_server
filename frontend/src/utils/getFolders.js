import { API } from "../core/config";

const getFolders = async () => {
  const resp = await fetch(`${API}/Settings/get_folders`, {
    method: "GET",
    headers: {
      Accept: "application/json",
    },
  });
  const json = await resp.json();
  return json;
};

export default getFolders;
