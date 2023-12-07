import { API } from "../core/config";

const updateFolders = async (folders) => {
  const resp = await fetch(`${API}/Settings/set_folders`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(folders),
  });
  const json = await resp.json();
  return json;
};

export default updateFolders;
