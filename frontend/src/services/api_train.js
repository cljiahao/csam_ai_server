import { createRequestOptions, sendRequest } from ".";

export const getSettings = async (item) => {
  const url = `/api/${item}`;
  const options = createRequestOptions("GET");
  return await sendRequest(url, options);
};
