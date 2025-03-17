import { createRequestOptions, sendRequest } from ".";

export const getItemType = async (lotNo) => {
  const params = new URLSearchParams({
    lot_no: lotNo,
  });
  const url = `/api/item?${params.toString()}`;
  const options = createRequestOptions("GET");
  return await sendRequest(url, options);
};

export const getProcessedCount = async (mode, lotNo, plate) => {
  const params = new URLSearchParams({
    lot_no: lotNo,
    plate_no: plate,
  });
  const url = `/api/count/${mode}?${params.toString()}`;
  const options = createRequestOptions("GET");
  return await sendRequest(url, options);
};
