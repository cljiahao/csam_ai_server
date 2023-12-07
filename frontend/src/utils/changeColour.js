import { marker } from "../core/config";

const changeColour = (zone, key, array, info, state) => {
  let target = array.chips[zone][key];
  const fol_dict = state.folders;
  const colors = Object.values(fol_dict);
  const folders = Object.keys(fol_dict);
  const index = colors.indexOf(target.color);

  Object.assign(marker.color, state.folders);

  if (index < 0) {
    target.color = marker.color[folders[0]];
    target.radius = marker.radius.highlight;
    target.border = marker.border.highlight;
    array.real_ng[folders[0]][key] = target.fname;
    info.no_of_real_ng[`no_of_${folders[0]}`] += 1;
  } else if (index === colors.length - 1) {
    target.color = marker.color.default;
    target.radius = marker.radius.default;
    target.border = marker.border.default;
    delete array.real_ng[folders[index]][key];
    info.no_of_real_ng[`no_of_${folders[index]}`] -= 1;
  } else {
    target.color = marker.color[folders[index + 1]];
    delete array.real_ng[folders[index]][key];
    array.real_ng[folders[index + 1]][key] = target.fname;
    info.no_of_real_ng[`no_of_${folders[index]}`] -= 1;
    info.no_of_real_ng[`no_of_${folders[index + 1]}`] += 1;
  }

  return [array, info];
};

export default changeColour;
