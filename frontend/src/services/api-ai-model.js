import { createRequestOptions, sendRequest } from ".";

export const getAllModelHistory = async (item) => {
  const params = new URLSearchParams({
    item: item,
  });
  const url = `/api/ai_model/model_history?${params}`;
  const options = createRequestOptions("GET");
  return await sendRequest(url, options);
};
