import { cn } from "@/lib/utils";

const DescriptiveHeader = ({ className, title, description }) => {
  return (
    <header className={cn("flex h-full w-full flex-col px-6", className)}>
      <h1 className="text-3xl font-bold underline">{title}</h1>
      <h2 className="text-xl">{description}</h2>
    </header>
  );
};

export default DescriptiveHeader;
