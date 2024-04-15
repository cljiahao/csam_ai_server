import { API } from "../core/config";

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
