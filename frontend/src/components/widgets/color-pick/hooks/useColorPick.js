import { useEffect, useState } from "react";
import { v4 as uuidv4 } from "uuid";

const useColorPick = (colorData) => {
  const [labelColors, setLabelColors] = useState([]);
  const [error, setError] = useState({ label: false, color: false });

  useEffect(() => {
    setLabelColors(colorData);
  }, [colorData]);

  const handleNewAdd = () => {
    setLabelColors((state) => [
      ...state,
      { uuid: uuidv4(), label: "", color: "#000000" },
    ]);
  };

  const handleDelete = (e) => {
    setLabelColors(
      labelColors.filter((item) => item.uuid !== e.currentTarget.id),
    );
  };

  const handleLabelColorChange = (e, type) => {
    const value = e.target.value;
    const id = e.target.id;

    const propExists = labelColors.some((obj) => obj[type] === value);
    const props = labelColors.map((item) => item[type]);
    const uniqueProps = new Set(props);
    setError((state) => ({
      ...state,
      [type]: propExists || props.length !== uniqueProps.size,
    }));
    setLabelColors((state) => {
      return state.map((item) => {
        if (item.uuid === id) {
          return { ...item, [type]: value };
        }
        return item;
      });
    });
  };

  const onChangeLabel = (e) => handleLabelColorChange(e, "label");
  const onChangeColor = (e) => handleLabelColorChange(e, "color");

  return {
    state: { error, labelColors },
    action: { handleNewAdd, handleDelete, onChangeColor, onChangeLabel },
  };
};

export default useColorPick;
