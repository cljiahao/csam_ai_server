import { forwardRef, useImperativeHandle } from "react";

import LabelValue from "@/components/static/label-value";
import { Button } from "@/components/ui/button";
import { Label } from "@/components/ui/label";
import { cn } from "@/lib/utils";
import ColorCard from "./components/ColorCard";
import ColorPickContext from "./contexts/useColorPickContext";
import useColorPick from "./hooks/useColorPick";

const ColorPick = forwardRef(({ className, colorData, label, value }, ref) => {
  const colorPickState = useColorPick(colorData);
  const {
    state: { error, labelColors },
    action: { handleNewAdd, handleDelete, onChangeColor, onChangeLabel },
  } = colorPickState;

  useImperativeHandle(ref, () => ({
    get labelColors() {
      return labelColors;
    },
  }));

  return (
    <ColorPickContext.Provider
      value={{ labelColors, handleDelete, onChangeColor, onChangeLabel }}
    >
      <div
        className={cn("hw-full flex flex-col gap-1 overflow-hidden", className)}
      >
        <div className="flex-between w-full">
          <LabelValue
            className="flex-start w-3/4"
            label={label}
            value={value}
            toColumn
          />
          <Button
            className="flex-center w-1/4"
            onClick={handleNewAdd}
            variant="default"
          >
            Add
          </Button>
        </div>
        {(error.color || error.label) && (
          <Label className="flex-center text-lg text-red-500">
            Duplicate found
          </Label>
        )}
        <div className="hw-full no-scrollbar flex flex-col overflow-y-auto">
          {labelColors?.map((obj) => {
            return <ColorCard key={obj?.uuid} id={obj?.uuid} />;
          })}
        </div>
      </div>
    </ColorPickContext.Provider>
  );
});

ColorPick.displayName = "ColorPick";

export default ColorPick;
