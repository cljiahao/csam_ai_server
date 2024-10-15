import { API } from "../core/config";

export const getItemType = async (lot_no) => {
  const res = await fetch(`${API}/get_item`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ lot_no: lot_no }),
  });
  return res;
};

export const addLocalDB = async (type, details, real_ng) => {
  const res = await fetch(`${API}/${type}/add_local_db`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(Object.assign(details, real_ng)),
  });
  return res;
};

export const unzip_files = async (file) => {
  const formData = new FormData();
  formData.append("file", file);
  const res = await fetch(`${API}/unzip_files`, {
    method: "POST",
    headers: {
      Accept: "application/json",
    },
    body: formData,
  });
  return res;
};

export const upload_settings = async (file) => {
  const formData = new FormData();
  formData.append("file", file);
  const res = await fetch(`${API}/upload_settings`, {
    method: "POST",
    headers: {
      Accept: "application/json",
    },
    body: formData,
  });
  return res;
};
