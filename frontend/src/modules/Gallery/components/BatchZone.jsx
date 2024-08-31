import { Label } from "@/components/ui/label";
import { Separator } from "@/components/ui/separator";

const BatchZone = ({ batch_no, children }) => {
  return (
    <div className="flex flex-col gap-2">
      <Label className="text-xl font-semibold">Batch: {batch_no}</Label>
      <Separator className="h-[0.15em] rounded-xl" />
      {children}
    </div>
  );
};

export default BatchZone;
