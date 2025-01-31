import React, { useEffect, useRef, useState } from "react";
import { AppContext } from "../../contexts/context";
import { MdOutlineUploadFile } from "react-icons/md";
import { MdOutlineMoveToInbox } from "react-icons/md";
import Swal from "sweetalert2";

import {
  initialArray,
  initialDetails,
  initialFocus,
  initialTrigger,
} from "../../core/config";
import Menu from "../../common/containers/Menu/Menu";
import NavBar from "../../common/components/NavBar";
import ImageHolder from "../../common/containers/ImageHolder/ImageHolder";
import Gallery from "../../common/containers/Gallery/Gallery";
import MenuChildren from "./containers/MenuChildren/MenuChildren";
import { dataProcess, imgErrorHandle } from "../../utils/dataHandle";
import { changeColor } from "../../utils/changeColor";
import { addLocalDB, getItemType } from "../../utils/api_data";
import { setFolColor } from "../../utils/api_images";

function CDC() {
  const [array, setArray] = useState(initialArray);
  const [details, setDetails] = useState(initialDetails);
  const [focus, setFocus] = useState(initialFocus);
  const [trigger, setTrigger] = useState(initialTrigger);
  const currentRealNG = useRef();
  const currentDetails = useRef();

  const type = "CDC";

  useEffect(() => {
    window.addEventListener("beforeunload", save);
    return () => {
      window.removeEventListener("beforeunload", save);
    };
  }, []);

  useEffect(() => {
    currentDetails.current = details;
  }, [details]);

  useEffect(() => {
    currentRealNG.current = { selected: array.selected };
  }, [array]);

  const openMenu = () => {
    if (trigger.menu && details.item) {
      setFolColor(details.item, array.folders);
    }
    setTrigger((prevTrigger) => ({
      ...prevTrigger,
      menu: !prevTrigger.menu,
    }));
  };

  const reset = () => {
    setArray(initialArray);
    setFocus(initialFocus);
    setTrigger(initialTrigger);
  };

  const save = async () => {
    if (currentDetails.current.lot) {
      const res = await addLocalDB(
        type,
        currentDetails.current,
        currentRealNG.current,
      );
      if (res) {
        Swal.fire({
          icon: "success",
          title: "Completed!",
          text: "Images saved, please proceed to next plate.",
        });
      } else {
        Swal.fire({
          icon: "error",
          title: "Oops...",
          text: "Error in saving images. Please consult technician.",
        });
      }
    }
  };

  const process = async (e) => {
    e.preventDefault();
    await save();
    reset();

    setTrigger({ ...trigger, image: "assets/loading.gif", error: false });

    if (
      !details.lot ||
      (details.plate && details.plate.slice(0, 3).toLowerCase() === "end")
    ) {
      details.lot = prompt("Please scan or Input Lot Number.");
      const res = await getItemType(details.lot);
      const item = await res.json();
      if (res.status === 521) {
        setTrigger({
          ...trigger,
          image: "assets/error_lot_no.png",
          error: true,
        });
      } else if (!item) {
        details.item = prompt("Please scan or Input Item Code");
      } else {
        details.item = item;
      }
    }

    const file = e.target.files[0];
    if (file && !trigger.error) {
      details.plate = file.name.split(".")[0];
      setDetails(details);
      const res = await imgErrorHandle(file, details, type);
      setTrigger({ ...trigger, image: res.image, error: res.error });
      if (!res.error) {
        const [new_array, new_details] = await dataProcess(
          res.json,
          array,
          details,
        );
        setArray(new_array);
        setDetails(new_details);
      } else {
        details.lot = "";
        setDetails(details);
      }
    }
  };

  const highlight = (zone, key) => {
    const new_selected = changeColor(zone, key, array, details);
    setArray({ ...array, selected: new_selected });
  };

  const upload_info = {
    upload: {
      name: "Upload",
      type: "file",
      icon: <MdOutlineUploadFile />,
      style: { font: "text-3xl" },
      accept: ".png, .jpg, .jpeg",
      onClick: (e) => {
        e.currentTarget.value = "";
      },
      onChange: process,
    },
    submit: {
      name: "Submit",
      type: "button",
      icon: <MdOutlineMoveToInbox />,
      style: { font: "text-3xl" },
      onClick: save,
    },
  };

  const detail_info = {
    lot: {
      name: "Lot No:",
      data: details.lot,
    },
    plate: {
      name: "Plate No:",
      data: details.plate,
    },
    select: {
      name: "Selected:",
      data:
        Object.keys(details.real_ng).length === 0
          ? 0
          : Object.values(details.real_ng).reduce((a, b) => a + b, 0),
      unit: "pcs",
    },
  };

  return (
    <AppContext.Provider
      value={{
        array,
        setArray,
        details,
        setDetails,
        focus,
        setFocus,
        trigger,
        setTrigger,
        type,
      }}
    >
      <main className="flex h-screen max-h-screen w-screen">
        <section className="w-full">
          <div className="flex h-full w-full flex-col justify-center overflow-scroll overflow-x-hidden overflow-y-hidden">
            {trigger.image ? (
              <ImageHolder highlight={highlight} />
            ) : (
              <div className="m-auto mx-10 h-5/6 rounded-xl border-4 border-dashed border-gray-400 bg-gray-100" />
            )}
          </div>
        </section>
        <aside className="relative flex h-full w-[60%] flex-col border-l-2 border-slate-400">
          <NavBar
            openMenu={openMenu}
            upload_info={upload_info}
            detail_info={detail_info}
          />
          <Gallery highlight={highlight} />
          <Menu
            openMenu={openMenu}
            menu={trigger.menu}
            children={<MenuChildren />}
          />
        </aside>
      </main>
    </AppContext.Provider>
  );
}

export default CDC;
