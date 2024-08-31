import {
  useDisplayContext,
  useImageDetailsContext,
} from "@/contexts/csamContext";
import CanvasOnImage from "./components/CanvasOnImage/CanvasOnImage";
import useDisplayEvent from "./hooks/useDisplayEvent";
import Placeholder from "./components/Placeholder";
import Error from "@/components/Error/Error";
import Loading from "@/components/Loading/Loading";

const ImageHolder = () => {
  const { ref } = useDisplayContext();
  const { imageDetails } = useImageDetailsContext();
  const [UpdateInitialDisplay, UpdateResizeWindow] = useDisplayEvent();

  // TODO : Remove below 2 functions and use at Hook instead
  // Update state with ref width and height at the beginning
  UpdateInitialDisplay();
  // Update state with ref width and height when window resize
  UpdateResizeWindow();

  if (imageDetails.detail) return <Error message={imageDetails.detail} />;
  if (imageDetails.isLoading) return <Loading />;

  return (
    <div className="hw-full flex overflow-hidden" ref={ref}>
      {imageDetails.image ? (
        <CanvasOnImage />
      ) : (
        <Placeholder>{imageDetails.detail}</Placeholder>
      )}
    </div>
  );
};

export default ImageHolder;
