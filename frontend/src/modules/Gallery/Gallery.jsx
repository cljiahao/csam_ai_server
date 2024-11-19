import { MARKERS } from "@/core/config";
import { useCanvasContext, useImageDetailsContext } from "@/contexts/context";
import { Label } from "@/components/ui/label";
import { Separator } from "@/components/ui/separator";
import Thumbnails from "./components/Thumbnails";

const Gallery = ({ page }) => {
  const { imageDetails } = useImageDetailsContext();
  const { marks } = useCanvasContext();

  // Return null if directory is not available
  if (!imageDetails.directory) return null;

  const imageInfo = marks.reduce((acc, { batch, id, circle }) => {
    if (MARKERS.zoom === circle) return acc;

    if (!acc[batch]) {
      acc[batch] = [];
    }

    const isMarkerZero = MARKERS.marks.some(
      ({ id: markerId }) => markerId === 0,
    );
    const isCDCPage = page.toUpperCase() === "CDC";

    if (isMarkerZero && isCDCPage) return acc;

    acc[batch].push(id);
    return acc;
  }, {});

  return (
    <div className="no-scrollbar hw-full flex flex-grow flex-col gap-3 overflow-y-scroll p-3">
      {!imageDetails.isLoading &&
        Object.keys(imageInfo).map((batch) => (
          <div key={batch} className="flex flex-col gap-2">
            <Label className="text-xl font-semibold">Batch: {batch}</Label>
            <Separator className="h-[0.15em] rounded-xl" />
            <Thumbnails page={page} thumbs_array={imageInfo[batch]} />
          </div>
        ))}
    </div>
  );
};

export default Gallery;
