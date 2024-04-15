import { marker } from "../core/config";

export const changeColor = (zone, key, array, details) => {
  let target = array.chips[zone][key];

  Object.assign(marker.color, array.folders);
  const folders = Object.keys(array.folders);
  const colors = Object.values(array.folders);
  const index = colors.indexOf(target.color);

  // Color is default
  if (index < 0) {
    target.color = marker.color[folders[0]];
    target.radius = marker.radius._highlight;
    target.border = marker.border._highlight;
    array.selected[folders[0]][key] = target.fname;
    details.real_ng[folders[0]] += 1;
  } else if (index === colors.length - 1) {
    target.color = marker.color._default;
    target.radius = marker.radius._default;
    target.border = marker.border._default;
    delete array.selected[folders[index]][key];
    details.real_ng[folders[index]] -= 1;
  } else {
    target.color = marker.color[folders[index + 1]];
    delete array.selected[folders[index]][key];
    array.selected[folders[index + 1]][key] = target.fname;
    details.real_ng[folders[index]] -= 1;
    details.real_ng[folders[index + 1]] += 1;
  }

  return array.selected;
};
