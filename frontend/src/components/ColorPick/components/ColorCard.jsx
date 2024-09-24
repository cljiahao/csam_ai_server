import { MdDelete } from "react-icons/md";

import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Input } from "@/components/ui/input";

const ColorCard = ({ id, card, updateInput, removeInput }) => {
  return (
    <Card className="flex-center relative h-20 w-full">
      <CardHeader className="h-full w-3/5 flex-col justify-center">
        <CardTitle>
          <Input
            id={id}
            name="category"
            type="text"
            className="border-0 p-0 text-2xl"
            value={card.category}
            onChange={updateInput}
          />
        </CardTitle>
        <CardDescription>{card.hex}</CardDescription>
      </CardHeader>
      <CardContent className="flex-center h-full w-2/5 p-0">
        <Button className="h-12 w-12 overflow-hidden rounded-full border-2">
          <Input
            id={id}
            name="hex"
            type="color"
            className="h-full w-full scale-[50] p-0"
            value={card.hex}
            onChange={updateInput}
          />
        </Button>
      </CardContent>
      <MdDelete
        className="absolute right-2 top-2 cursor-pointer"
        onClick={() => removeInput(id)}
      />
    </Card>
  );
};

export default ColorCard;
