import { API } from "../core/config";

export const uploadImage = async (file, details, type) => {
  const formData = new FormData();
  formData.append("lot_no", details.lot);
  formData.append("item", details.item);
  formData.append("file", file);

  const res = await fetch(`${API}/${type}/upload_file`, {
    method: "POST",
    headers: {
      Accept: "application/json",
    },
    body: formData,
  });
  return res;
};

export const getFolColor = async (item) => {
  const res = await fetch(`${API}/get_fol_color`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ item: item }),
  });
  const json = await res.json();
  return json;
};

export const setFolColor = async (item, color) => {
  const res = await fetch(`${API}/set_fol_color`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ item: item, color: color }),
  });
  return res;
};

export const setCache = async (type) => {
  const res = await fetch(`${API}/${type}/set_cache`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({}),
  });
  return res;
};
