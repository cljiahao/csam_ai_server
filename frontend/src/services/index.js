export const sendRequest = async (url, options) => {
  try {
    const response = await fetch(url, options);
    const result = await response.json();
    if (!response.ok)
      throw new Error(
        result.detail || { details: "An error occurred while fetching data." },
      );
    return result;
  } catch (error) {
    console.error("Request failed:", JSON.stringify(error));
    throw error; // Re-throw to let TanStack Query handle errors
  }
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
