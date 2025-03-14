import { createRequestOptions, sendRequest } from ".";

export const getItemType = async (lotNo) => {
  const url = `/api/item?lot_no=${lotNo}`;
  const options = createRequestOptions("GET");
  return await sendRequest(url, options);
};

export const getImageSrc = async (src_path) => {
  const url = `/api/image/${src_path}`;
  const options = createRequestOptions("GET");
  return await sendRequest(url, options);
};

export const getProcessedCount = async (mode, lotNo, plate) => {
  const url = `/api/count/${mode}?lot_no=${lotNo}&plate_no=${plate}`;
  const options = createRequestOptions("GET");
  return await sendRequest(url, options);
};
