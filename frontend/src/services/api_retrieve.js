import { sendRequest } from ".";

export const getItemType = async (lot_no) => {
  return await sendRequest(`${__API_URL__}/item/${lot_no}`);
};

export const getImageSrc = async (src_path) => {
  return await sendRequest(`${__API_URL__}/image/${src_path}`);
};

export const getProcessedCount = async (mode, lot_no, plate) => {
  return await sendRequest(`${__API_URL__}/count/${mode}/${lot_no}/${plate}`);
};
