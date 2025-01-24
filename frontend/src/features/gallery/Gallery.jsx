import { useLocation } from "react-router-dom";

import { Label } from "@/components/ui/label";
import { Separator } from "@/components/ui/separator";
import Thumbnail from "./components/Thumbnail";
import useThumbnailHandlers from "./hooks/useThumbnailHandlers";

const Gallery = () => {
  const location = useLocation();
  const mode = location.pathname.split("/").pop();

  const {
    state: { processImageData, marksFileNames },
  } = useThumbnailHandlers();

  return (
    <div className="no-scrollbar hw-full flex flex-grow flex-col gap-3 overflow-y-scroll p-3">
      {processImageData?.defect_batches?.map((defect_batch) => (
        <div key={defect_batch.batch_no} className="flex flex-col gap-2">
          <Label className="text-xl font-semibold">
            Batch: {defect_batch.batch_no}
          </Label>
          <Separator className="h-[0.15em] rounded-xl" />
          <div className="hw-full grid grid-cols-8 gap-3">
            {defect_batch?.defect_files
              ?.filter((file) => {
                if (mode === "CDC" && marksFileNames.has(file.file_name))
                  return true;
                return false;
              })
              .map((file) => {
                return (
                  <Thumbnail
                    key={file.file_name}
                    directory={processImageData?.directory}
                    defect_mode={file.defect_mode}
                    file_name={file.file_name}
                  />
                );
              })}
          </div>
        </div>
      ))}
    </div>
  );
};

export default Gallery;
