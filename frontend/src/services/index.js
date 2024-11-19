export const sendRequest = async (url, options) => {
  return await fetch(url, options);
};

export const createRequestOptions = (method, body) => {
  return {
    method,
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(body),
  };
};

export const createFileRequestOptions = (method, body) => {
  return {
    method,
    headers: {
      Accept: "application/json",
    },
    body: body,
  };
};
