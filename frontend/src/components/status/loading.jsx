import { cn } from "@/lib/utils";

const Loading = ({ className, message = "Loading..." }) => {
  return (
    <div
      className={cn(
        "flex h-full w-full flex-col items-center justify-center bg-gray-100",
        className,
      )}
    >
      <div className="mb-4 h-16 w-16 animate-spin rounded-full border-t-4 border-solid border-blue-500"></div>
      <p className="text-lg text-gray-700">{message}</p>
    </div>
  );
};

export default Loading;
