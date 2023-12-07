import { marker } from "../core/config";

const dataProcess = (json, array, data, focus, info, state) => {
  const chips = json.chips;
  const settings = json.settings;
  const fol_dict = settings;
  const folders = Object.keys(fol_dict);

  Object.assign(marker.color, fol_dict);

  let no_of_real_ng = Object.assign(
    {},
    ...folders.map((key) => {
      return { [`no_of_${key}`]: 0 };
    }),
  );

  Object.keys(chips).map((key, index) => {
    return (chips[key] = Object.assign(
      {},
      ...json.chips[key].map((filename) => {
        const img_name = filename.split(".")[0];
        const [class_type, , id, x, y] = img_name.split("_");
        const fname = filename;

        let color = marker.color.default;
        let radius = marker.radius.default;
        let border = marker.border.default;

        if (class_type !== "0") {
          color = marker.color[folders[class_type - 1]];
          radius = marker.radius.highlight;
          border = marker.border.highlight;
          no_of_real_ng[`no_of_${folders[class_type - 1]}`] += 1;
          array.no_of_real_ng[folders[class_type - 1]][id] = fname;
        }

        return {
          [id]: { class_type, x, y, color, fname, radius, border },
        };
      }),
    ));
  });
  array.chips = chips;
  Object.keys(fol_dict).map((k, i) => (array.real_ng[k] = {}));

  data.plate_no = json.plate_no;
  data.directory = json.directory;
  data.chip_type = json.chip_type;

  if (
    data.plate_no.slice(0, 3)[0].toLowerCase() === "end" ||
    data.lot_no === null
  )
    data.lot_no = "";

  const img_shape = json.img_shape;
  focus.img_shape = { width: img_shape[0], height: img_shape[1] };

  info.no_of_batches = json.no_of_batches;
  info.no_of_chips = json.no_of_chips;
  info.no_of_real_ng = no_of_real_ng;
  info.no_of_pred_ng = json.no_of_pred;

  state.error = false;
  state.menu = false;
  state.folders = fol_dict;

  return [array, data, focus, info, state];
};

export default dataProcess;
