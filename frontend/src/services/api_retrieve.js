import { createRequestOptions, sendRequest } from ".";

export const getItemType = async (lot_no) => {
  const url = `/api/item/${lot_no}`;
  const options = createRequestOptions("GET");
  return await sendRequest(url, options);
};

export const getImageSrc = async (src_path) => {
  const url = `/api/image/${src_path}`;
  const options = createRequestOptions("GET");
  return await sendRequest(url, options);
};

export const getProcessedCount = async (mode, lot_no, plate) => {
  const url = `/api/count/${mode}/${lot_no}/${plate}`;
  const options = createRequestOptions("GET");
  return await sendRequest(url, options);
};
