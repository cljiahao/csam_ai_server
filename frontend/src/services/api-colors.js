import { createRequestOptions, sendRequest } from ".";

export const getDotColors = async (item) => {
  const params = new URLSearchParams({ item });
  const url = `/api/color_pick/dot_colors?${params.toString()}`;
  const options = createRequestOptions("GET");
  return await sendRequest(url, options);
};

export const saveDotColors = async (item, dotColors) => {
  const params = new URLSearchParams({ item });
  const url = `/api/color_pick/dot_colors?${params.toString()}`;
  const options = createRequestOptions("POST", dotColors);
  return await sendRequest(url, options);
};
