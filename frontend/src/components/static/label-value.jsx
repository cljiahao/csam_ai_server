import { Label } from "@/components/ui/label";

const LabelValue = ({ label, value, toColumn = false }) => {
  return (
    <div
      className={`hw-full flex items-center ${toColumn ? "flex-col" : "grid grid-cols-3"}`}
    >
      <Label className="flex h-full items-center font-semibold">{label}</Label>
      <Label className="flex h-full items-center text-nowrap">{value}</Label>
    </div>
  );
};

export default LabelValue;
