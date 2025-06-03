import { forwardRef, useImperativeHandle, useState } from "react";
import { FaTrash } from "react-icons/fa";
import { v4 as uuidv4 } from "uuid";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { cn } from "@/lib/utils";
import useColorValidation from "./hooks/useColorPickFormValidate";

const ColorPick = forwardRef(({ className, item }, ref) => {
  const [colors, setColors] = useState([]);

  useImperativeHandle(ref, () => ({
    get colors() {
      return colors; // Always gets latest value
    },
    setColors,
  }));

  const { validateLabelChange, validateColorChange } = useColorValidation();

  const errors = colors.map((color, index) => ({
    defect_label: validateLabelChange(colors, index, color.defect_label) || "",
    hex_color: validateColorChange(colors, index, color.hex_color) || "",
  }));

  const handleAdd = () => {
    const newColor = { uuid: uuidv4(), defect_label: "", hex_color: "#ffff00" };
    setColors((prevState) => [...prevState, newColor]);
  };

  const handleRemove = (index) => {
    setColors((prevState) => prevState.filter((_, i) => i !== index));
  };

  const handleLabelChange = (index, newLabel) => {
    setColors((prevState) =>
      prevState.map((entry, i) =>
        i === index ? { ...entry, defect_label: newLabel } : entry,
      ),
    );
  };

  const handleColorChange = (index, newColor) => {
    setColors((prevState) =>
      prevState.map((entry, i) =>
        i === index ? { ...entry, hex_color: newColor } : entry,
      ),
    );
  };

  return (
    <div className={cn("flex h-full w-full flex-col items-center", className)}>
      <div className="text-m flex h-14 w-full items-center px-3 font-bold">
        Item: {item}
      </div>
      <div className="flex w-full flex-col space-y-2 px-3">
        <Button onClick={handleAdd} variant="default">
          Add
        </Button>
      </div>
      {colors.length > 0 && (
        <div className="mt-4 flex w-full flex-col items-center space-y-4 overflow-y-auto rounded-xl bg-slate-300 py-3">
          {colors.map((colorEntry, index) => (
            <div
              key={colorEntry.uuid}
              className="relative flex w-full flex-row space-x-4 px-3 pr-8"
            >
              <div className="flex flex-col space-y-1">
                <Input
                  type="text"
                  value={colorEntry.defect_label}
                  onChange={(e) => handleLabelChange(index, e.target.value)}
                  className="h-11 max-w-xs"
                  placeholder="Enter defect label"
                />
                <div className="h-5">
                  {errors[index]?.defect_label && (
                    <p className="text-sm text-red-500">
                      {errors[index].defect_label}
                    </p>
                  )}
                </div>
              </div>
              <div className="flex flex-col space-y-1">
                <Input
                  type="color"
                  value={colorEntry.hex_color}
                  onChange={(e) => handleColorChange(index, e.target.value)}
                  className="h-11 w-12 border-none p-0"
                />
                <div className="h-5">
                  {errors[index]?.hex_color && (
                    <p className="text-sm text-red-500">
                      {errors[index].hex_color}
                    </p>
                  )}
                </div>
              </div>
              <button
                onClick={() => handleRemove(index)}
                className="absolute right-0 top-0 p-2"
              >
                <FaTrash className="h-4 w-4 text-black" />
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
});

ColorPick.displayName = "ColorPick";

export default ColorPick;
