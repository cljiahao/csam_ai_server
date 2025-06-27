import { toast } from "@/hooks/use-toast";

const showUploadToast = (item, lotNo, fileName) => {
  toast({
    title: "You submitted the following values:",
    description: (
      <pre className="mt-2 flex w-[340px] flex-col rounded-md bg-slate-950 p-4">
        <kbd className="text-white">Lot No: {lotNo}</kbd>
        <kbd className="text-white">Item: {item}</kbd>
        <kbd className="text-white">File Name: {fileName}</kbd>
      </pre>
    ),
    duration: 2000,
  });
};

export default showUploadToast;
