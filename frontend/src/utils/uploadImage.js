import { API } from "../core/config";

const uploadImage = async (file, data, type) => {
  const formData = new FormData();
  formData.append("file", file);
  formData.append("lot_no", data.lot_no);

  const res = await fetch(`${API}/${type}/upload_file`, {
    method: "POST",
    headers: {
      Accept: "application/json",
    },
    body: formData,
  });
  return res;
};

export default uploadImage;
