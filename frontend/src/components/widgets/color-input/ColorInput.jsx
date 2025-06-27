import { Input } from "@/components/ui/input";
import { cn } from "@/lib/utils";

const ColorInput = ({ className, id, value, onChange }) => {
  return (
    <div className="flex-center h-full">
      <div
        className={cn(
          "flex-center h-12 w-12 overflow-hidden rounded-full border-2",
          className,
        )}
      >
        <Input
          className="hw-full scale-150 border-0 p-0"
          id={id}
          type="color"
          value={value}
          onChange={onChange}
        />
      </div>
    </div>
  );
};

export default ColorInput;
