import { createFileRequestOptions, createRequestOptions, sendRequest } from ".";

export const uploadImage = async (mode, item, lotNo, formData) => {
  const url = `/api/upload/image/${mode}/${item}/${lotNo}`;
  const options = createFileRequestOptions("POST", formData);
  return await sendRequest(url, options);
};

export const saveFinalJudgement = async (data) => {
  const url = `/api/upload/save`;
  const options = createRequestOptions("POST", data);
  return await sendRequest(url, options);
};
