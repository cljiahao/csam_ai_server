import { createFileRequestOptions, createRequestOptions, sendRequest } from ".";

export const getImageSrc = async (src_path) => {
  const url = `/api/csam_image/${src_path}`;
  const options = createRequestOptions("GET");
  return await sendRequest(url, options);
};

export const uploadImage = async (mode, item, lotNo, formData) => {
  const params = new URLSearchParams({
    item: item,
    lot_no: lotNo,
  });
  const url = `/api/csam_image/process_image/${mode}?${params.toString()}`;
  const options = createFileRequestOptions("POST", formData);
  return await sendRequest(url, options);
};

export const saveFinalJudgement = async (mode, item, lotNo, data) => {
  const params = new URLSearchParams({
    item: item,
    lot_no: lotNo,
  });
  const url = `/api/csam_image/save_local/${mode}?${params.toString()}`;
  const options = createRequestOptions("POST", data);
  return await sendRequest(url, options);
};
