import { API } from "../core/config";

const sendData = async (array, data, info, type) => {
  const send_data = {
    lot_no: data.lot_no,
    plate_no: data.plate_no,
    directory: data.directory,
    chip_type: data.chip_type,
    real_ng_dict: array.real_ng,
    no_of_batches: info.no_of_batches,
    no_of_chips: info.no_of_chips,
    no_of_pred_ng: info.no_of_pred_ng,
    no_of_real_ng: info.no_of_real_ng,
  };

  await fetch(`${API}/${type}/insert_db`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(send_data),
  });
};

export default sendData;
