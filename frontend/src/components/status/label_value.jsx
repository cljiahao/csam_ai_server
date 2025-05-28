import { Label } from "@/components/ui/label";
import { cn } from "@/lib/utils";

const LabelValue = ({ className, label, value, toColumn = false }) => {
  return (
    <div
      className={cn(
        "flex h-full w-full items-center gap-1 p-2",
        toColumn ? "flex-col" : "grid grid-cols-3",
        className,
      )}
    >
      <Label
        className={cn(
          "h-full w-full font-semibold",
          toColumn ? "flex-center" : "flex",
        )}
      >
        {label}:
      </Label>
      <Label
        className={cn(
          "h-full w-full overflow-hidden text-clip",
          toColumn ? "flex-center" : "col-span-2 flex",
        )}
      >
        {value}
      </Label>
    </div>
  );
};

export default LabelValue;
