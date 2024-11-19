import { IconContext } from "react-icons";
import { FaPlus } from "react-icons/fa";

import { Button } from "@/components/ui/button";
import ColorCard from "./components/ColorCard";
import { useColorPick } from "./hooks/useColorPick";

// TODO: Make colorpick dynamic and easy to detach

const ColorPick = ({ children, itemType }) => {
  const [colorSet, addFolderHex, removeFolderHex, updateFolderHex] =
    useColorPick({ itemType });
  return (
    <IconContext.Provider value={{ size: "1em" }}>
      <div className="flex h-[calc(100vh-90px)] flex-col">
        <div className="flex-center h-20 w-full gap-3 pb-5 pt-3">
          {children}
          <Button onClick={addFolderHex}>
            <FaPlus />
          </Button>
        </div>
        <div className="no-scrollbar flex flex-col gap-1 overflow-scroll">
          {colorSet?.colors.map((card, index) => (
            <ColorCard
              key={index}
              id={index}
              card={card}
              updateInput={updateFolderHex}
              removeInput={removeFolderHex}
            />
          ))}
        </div>
      </div>
    </IconContext.Provider>
  );
};

export default ColorPick;
