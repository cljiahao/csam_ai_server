import React, { useContext } from "react";
import { AppContext } from "../../../contexts/context";
import { API, FOCUS_SCALE, marker } from "../../../core/config";

const Thumbnails = ({ highlight, zone }) => {
  const { array, data, focus, state, setArray, setFocus, type } =
    useContext(AppContext);
  const selected = {};
  type === "CDC"
    ? Object.values(array.real_ng).map((v, i) => Object.assign(selected, v))
    : Object.assign(selected, array.chips[zone]);
  const chips = array.chips[zone];
  const folders = Object.keys(state.folders);

  const focusOnChip = (e, key, zone) => {
    const coords = e.target.alt.split(".")[0];
    const [x, y] = coords.split("_").slice(-2);
    setFocus({ ...focus, state: true, x: x, y: y, scale: FOCUS_SCALE });
    let target = array.chips[zone][key];
    if (target.color == null) {
      target.color = marker.color.zoom;
      target.radius = marker.radius.zoom;
      setArray({ ...array, array: { ...array.chips, [key]: target } });
    }
  };

  const unfocusOnChip = (key, zone) => {
    setFocus({ ...focus, state: false, x: 0, y: 0, scale: 1 });
    let target = array.chips[zone][key];
    if (target.color === "chartreuse") {
      target.color = marker.color.default;
      target.radius = marker.radius.default;
      setArray({ ...array, array: { ...array.chips, [key]: target } });
    }
  };
  // TODO: Caching of images
  // TODO: Lazing Loading or Pagination to improve speed
  return (
    <div
      className="grid grid-cols-5 gap-x-5 gap-y-5 p-3 xl:grid-cols-8"
      key={zone}
    >
      {Object.keys(chips).map((k) => {
        return (
          <>
            {k in selected && (
              <img
                className="scale-125 transform cursor-pointer border-4"
                key={k}
                src={`${API}${data.directory.split("backend")[1]}/${
                  chips[k].class_type !== "0"
                    ? folders[chips[k].chip_type - 1]
                    : "temp"
                }/${chips[k].fname}`}
                alt={chips[k].fname}
                style={{ border: chips[k].border }}
                onClick={() => highlight(zone, k)}
                onMouseEnter={(e) => focusOnChip(e, k, zone)}
                onMouseLeave={() => unfocusOnChip(k, zone)}
              />
            )}
          </>
        );
      })}
    </div>
  );
};

export default Thumbnails;
