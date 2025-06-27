import { Label } from "@/components/ui/label";
import { cn } from "@/lib/utils";

const LabelValue = ({ className, label, value, toColumn = false }) => {
  return (
    <div
      className={cn(
        "flex h-full w-full items-center",
        toColumn ? "flex-col" : "grid grid-cols-3",
        className,
      )}
    >
      <Label className="flex h-full items-center">{label}</Label>
      <Label className="col-span-2 flex h-full items-center overflow-hidden text-nowrap">
        {value}
      </Label>
    </div>
  );
};

export default LabelValue;
