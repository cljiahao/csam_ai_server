import { API_URL } from "@/core/config";
import { sendRequest } from ".";

export const getItemType = async (lot_no) => {
  return await sendRequest(`${API_URL}/item/${lot_no}`);
};

export const getImageSrc = async (src_path) => {
  return await sendRequest(`${API_URL}/image/${src_path}`);
};

export const getProcessedCount = async (mode, lot_no, plate) => {
  return await sendRequest(`${API_URL}/count/${mode}/${lot_no}/${plate}`);
};
