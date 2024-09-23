import { useCanvasContext, useImageDetailsContext } from "@/contexts/context";
import { Label } from "@/components/ui/label";
import { Separator } from "@/components/ui/separator";

import Thumbnails from "./components/Thumbnails";

const Gallery = ({ mode }) => {
  const { imageDetails } = useImageDetailsContext();
  const { marks, markers } = useCanvasContext();

  // Return null if directory is not available
  if (!imageDetails.directory) return null;

  const imageInfo = marks?.reduce((acc, { batch, id, circle }) => {
    if (markers.zoom !== circle) {
      if (!acc[batch]) {
        acc[batch] = [];
      }
      if (
        markers.marks.find(({ id: markerId }) => markerId === 0) === circle &&
        mode.toUpperCase() === "CDC"
      )
        return acc;
      acc[batch].push(id);
    }
    return acc;
  });

  return (
    <div className="no-scrollbar hw-full flex flex-grow flex-col gap-3 overflow-y-scroll p-3">
      {!imageDetails.isLoading &&
        Object.keys(imageInfo).map((batch) => (
          <div key={batch} className="flex flex-col gap-2">
            <Label className="text-xl font-semibold">Batch: {batch}</Label>
            <Separator className="h-[0.15em] rounded-xl" />
            <Thumbnails mode={mode} thumbs_array={imageInfo[batch]} />
          </div>
        ))}
    </div>
  );
};

export default Gallery;
