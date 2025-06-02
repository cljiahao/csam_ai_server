import { createRequestOptions, sendRequest } from ".";

export const getDotColors = async (item) => {
  const params = new URLSearchParams({ item });
  const url = `/api/color_pick/dot_colors?${params.toString()}`;
  const options = createRequestOptions("GET");
  return await sendRequest(url, options);
};

export const saveDotColors = async (itemDotColors) => {
  const url = `/api/color_pick/dot_colors`;
  const options = createRequestOptions("POST", itemDotColors);
  return await sendRequest(url, options);
};
