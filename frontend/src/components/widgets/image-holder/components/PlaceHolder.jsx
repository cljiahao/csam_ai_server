import { cn } from "@/lib/utils";

const Placeholder = ({ className, text }) => {
  return (
    <div className={cn("h-full w-full", className)}>
      <div className="flex-center hw-full">
        <div className="flex-center h-[90%] w-[95%] rounded-xl border-4 border-dashed border-gray-400 bg-gray-100">
          <p className="text-bold text-5xl text-red-500">{text}</p>
        </div>
      </div>
    </div>
  );
};

export default Placeholder;
