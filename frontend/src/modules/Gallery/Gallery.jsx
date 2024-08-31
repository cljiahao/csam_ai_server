import Thumbnails from "./components/Thumbnails/Thumbnails";
import BatchZone from "./components/BatchZone";
import useImageInfo from "./hooks/useImageInfo";
import { useImageDetailsContext } from "@/contexts/csamContext";

const Gallery = ({ mode }) => {
  const { fileNames } = useImageInfo(mode);
  const { imageDetails } = useImageDetailsContext();

  // Return null if directory is not available
  if (!imageDetails.directory) return null;

  return (
    <div className="no-scrollbar hw-full flex flex-grow flex-col gap-3 overflow-y-scroll p-3">
      {!imageDetails.isLoading &&
        Object.keys(fileNames).map((batch) => (
          <BatchZone key={batch} batch_no={batch}>
            <Thumbnails mode={mode} thumbs_array={fileNames[batch]} />
          </BatchZone>
        ))}
    </div>
  );
};

export default Gallery;
