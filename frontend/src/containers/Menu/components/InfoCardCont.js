import React, { useContext } from "react";
import { AppContext } from "../../../contexts/context";
import { API } from "../../../core/config";
import InfoCard from "./InfoCard";

const InfoCardCont = () => {
  const { array, data, state } = useContext(AppContext);
  const folders = Object.keys(state.folders);
  return (
    <div className="grid grid-flow-row grid-cols-3 gap-10 px-7">
      {Object.keys(array.real_ng).map((key) => {
        const file_list = Object.values(array.real_ng[key]);
        if (file_list.length > 0) {
          const rand_file =
            file_list[Math.floor(Math.random() * file_list.length)];
          return (
            <InfoCard
              src={`${API}${data.directory.split("backend")[1]}/${
                rand_file[0] !== "0" ? folders[rand_file[0] - 1] : "temp"
              }/${rand_file}`}
              title={key}
              count={file_list.length}
            />
          );
        } else {
          return null;
        }
      })}
    </div>
  );
};

export default InfoCardCont;
