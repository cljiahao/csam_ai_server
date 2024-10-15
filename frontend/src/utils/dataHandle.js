import { API, marker } from "../core/config";
import { getFolColor, uploadImage } from "./api_images";

export const dataProcess = async (json, array, details) => {
  Object.assign(details, json.details);
  const fol_col = await getFolColor(details.item);
  Object.assign(marker.color, fol_col);
  Object.keys(fol_col).forEach((k) => {
    details.real_ng[k] = 0;
    array.selected[k] = {};
  });
  array.folders = fol_col;

  const chips = json.chips;
  Object.keys(chips).map((key) => {
    return (chips[key] = Object.assign(
      {},
      ...json.chips[key].map((fname) => {
        const img_name = fname.split(".")[0];
        const [class_type, , id, x, y] = img_name.split("_");

        let color = marker.color._default;
        let radius = marker.radius._default;
        let border = marker.border._default;

        if (class_type !== "0") {
          color = marker.color[Object.keys(fol_col)[class_type - 1]];
          radius = marker.radius._highlight;
          border = marker.border._highlight;
          details.real_ng[Object.keys(fol_col)[class_type - 1]] += 1;
          array.selected[Object.keys(fol_col)[class_type - 1]][id] = fname;
        }

        return {
          [id]: { class_type, x, y, fname, color, radius, border },
        };
      }),
    ));
  });
  array.chips = chips;

  return [array, details];
};

export const imgErrorHandle = async (file, details, type) => {
  const res = await uploadImage(file, details, type);

  if (res.status === 522) {
    return { error: true, image: "assets/error.png" };
  } else if (res.status === 520) {
    return { error: true, image: "assets/error.png" };
  } else {
    const json = await res.json();
    const directory = "/get_image" + json.details.directory.split("images")[1];
    return {
      error: false,
      image: `${API}${directory}/original/${file.name}`,
      json: json,
    };
  }
};
