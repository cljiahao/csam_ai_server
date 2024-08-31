export function coordsExtract(file_name) {
  const image_name = file_name.split(".")[0];
  return image_name.split("_").slice(-2);
}

export function defectModeExtract(file_name) {
  const image_name = file_name.split(".")[0];
  return image_name.split("_")[0];
}

export function defectBatchExtract(file_name) {
  const image_name = file_name.split(".")[0];
  return image_name.split("_")[1];
}
