import React, { useContext } from "react";
import { AppContext } from "../../../../contexts/context";
import { API, marker } from "../../../../core/config";

const Thumbnails = ({ highlight, zone }) => {
  const { array, setArray, details, focus, setFocus, type } =
    useContext(AppContext);
  const selected = {};
  type === "CDC"
    ? Object.values(array.selected).map((v) => Object.assign(selected, v))
    : Object.assign(selected, array.chips[zone]);
  const chips = Object.keys(array.chips[zone])
    .filter((key) => Object.keys(selected).includes(key))
    .reduce((obj, key) => {
      obj[key] = array.chips[zone][key];
      return obj;
    }, {});
  const folders = Object.keys(array.folders);

  const focusOnChip = (e, key, zone) => {
    const coords = e.target.alt.split(".")[0];
    const [x, y] = coords.split("_").slice(-2);
    setFocus({ ...focus, state: true, x: x, y: y, scale: 7 });
    let target = array.chips[zone][key];
    if (target.color === "transparent") {
      setArray({
        ...array,
        chips: {
          ...array.chips,
          [zone]: {
            ...array.chips[zone],
            [key]: {
              ...array.chips[zone][key],
              color: marker.color._zoom,
              radius: marker.radius._zoom,
            },
          },
        },
      });
    }
  };

  const unfocusOnChip = (key, zone) => {
    setFocus({ ...focus, state: false, x: 0, y: 0, scale: 1 });
    let target = array.chips[zone][key];
    if (target.color === "chartreuse") {
      setArray({
        ...array,
        chips: {
          ...array.chips,
          [zone]: {
            ...array.chips[zone],
            [key]: {
              ...array.chips[zone][key],
              color: marker.color._default,
              radius: marker.radius._default,
            },
          },
        },
      });
    }
  };

  return (
    <div
      className="grid grid-cols-5 gap-x-5 gap-y-5 p-3 xl:grid-cols-8"
      key={zone}
    >
      {Object.keys(chips).map((k) => {
        const directory = "/images" + details.directory.split("images")[1];
        const folder =
          chips[k]?.class_type === "0"
            ? "temp"
            : folders[chips[k]?.class_type - 1];
        const fname = chips[k]?.fname;
        return (
          <img
            key={k}
            className="2xl:border-3 scale-125 transform cursor-pointer"
            src={`${API}${directory}/${folder}/${fname}`}
            alt={fname}
            style={{ border: chips[k]?.border }}
            onClick={() => highlight(zone, k)}
            onMouseEnter={(e) => focusOnChip(e, k, zone)}
            onMouseLeave={() => unfocusOnChip(k, zone)}
          />
        );
      })}
    </div>
  );
};

export default Thumbnails;
