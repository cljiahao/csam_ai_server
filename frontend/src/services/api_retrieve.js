import { sendRequest } from ".";

export const getItemType = async (lot_no) => {
  return await sendRequest(`/api/item/${lot_no}`);
};

export const getImageSrc = async (src_path) => {
  return await sendRequest(`/api/image/${src_path}`);
};

export const getProcessedCount = async (mode, lot_no, plate) => {
  return await sendRequest(`/api/count/${mode}/${lot_no}/${plate}`);
};
