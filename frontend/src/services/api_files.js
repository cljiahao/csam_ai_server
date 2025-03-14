import { createFileRequestOptions, createRequestOptions, sendRequest } from ".";

export const uploadImage = async (mode, item, lotNo, formData) => {
  const params = new URLSearchParams({
    item: item,
    lot_no: lotNo
  });
  const url = `/api/upload/process_image/${mode}?${params.toString()}`;
  const options = createFileRequestOptions("POST", formData);
  return await sendRequest(url, options);
};

export const saveFinalJudgement = async (data) => {
  const url = `/api/upload/save_local`;
  const options = createRequestOptions("POST", data);
  return await sendRequest(url, options);
};