import { createFileRequestOptions, createRequestOptions, sendRequest } from ".";

export const uploadImage = async (form_data, mode, lot_no, item) => {
  const options = createFileRequestOptions("POST", form_data);
  return await sendRequest(
    `/api/upload/image/${mode}/${lot_no}/${item}`,
    options,
  );
};

export const saveFinalJudgement = async (data, mode, lot_no, plate, item) => {
  const options = createRequestOptions("POST", data);
  return await sendRequest(
    `/api/upload/save/${mode}/${lot_no}/${plate}/${item}`,
    options,
  );
};

export const uploadSettings = async (data) => {
  const options = createRequestOptions("POST", data);
  return await sendRequest(`/api/upload/settings`, options);
};

export const uploadZip = async (data) => {
  const options = createRequestOptions("POST", data);
  return await sendRequest(`/api/upload/zip`, options);
};
