import { API_URL } from "@/core/config";
import { createRequestOptions, sendRequest } from ".";

export const getAllFolColor = async () => {
  return await sendRequest(`${API_URL}/fol_color`);
};

export const getFolColor = async (item) => {
  return await sendRequest(`${API_URL}/fol_color/${item}`);
};

export const setAllFolColor = async (data) => {
  const options = createRequestOptions("POST", data);
  return await sendRequest(`${API_URL}/fol_color`, options);
};

export const setFolColor = async (item, data) => {
  const options = createRequestOptions("POST", data);
  return await sendRequest(`${API_URL}/fol_color/${item}`, options);
};
