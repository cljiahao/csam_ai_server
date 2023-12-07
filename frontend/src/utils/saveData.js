import Swal from "sweetalert2";
import { API } from "../core/config";

const saveData = async (array, data, info) => {
  const send_data = {
    lot_no: data.lot_no,
    plate_no: data.plate_no,
    directory: data.directory,
    chip_type: data.chip_type,
    real_ng_dict: array.real_ng,
    no_of_batches: info.no_of_batches,
    no_of_chips: info.no_of_chips,
    no_of_real_ng: info.no_of_real_ng,
  };

  const resp = await fetch(`${API}/CDC/save_images`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(send_data),
  });

  const alert = await resp.json();

  Swal.fire({
    title: alert.title,
    text: alert.text,
    icon: alert.icon,
    confirmButtonText: alert.confirmButtonText,
  });
};

export default saveData;
