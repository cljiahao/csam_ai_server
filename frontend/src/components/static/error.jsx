import { cn } from "@/lib/utils";

const Error = ({ className, message }) => {
  return (
    <div
      className={cn("flex-center h-full w-full bg-red-50 text-xl", className)}
    >
      <div
        className="rounded-lg border border-red-200 bg-red-100 px-4 py-3 text-red-800"
        role="alert"
      >
        <strong className="font-bold">Error: </strong>
        <span className="block sm:inline">{message}</span>
      </div>
    </div>
  );
};

export default Error;
