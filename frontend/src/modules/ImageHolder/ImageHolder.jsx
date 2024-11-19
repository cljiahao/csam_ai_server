import { useDisplayContext, useImageDetailsContext } from "@/contexts/context";
import Error from "@/components/Error";
import Loading from "@/components/Loading";
import Placeholder from "@/components/Placeholder";
import CanvasOnImage from "./components/CanvasOnImage";
import useDisplayEvent from "./hooks/useDisplayEvent";

// TODO: Make this dynamic component

const ImageHolder = () => {
  const { ref } = useDisplayContext();
  const { imageDetails } = useImageDetailsContext();
  const [UpdateInitialDisplay, UpdateResizeWindow] = useDisplayEvent();

  // Update state with ref width and height at the beginning
  UpdateInitialDisplay();
  // Update state with ref width and height when window resize
  UpdateResizeWindow();

  if (imageDetails.detail) return <Error message={imageDetails.detail} />;
  if (imageDetails.isLoading) return <Loading />;

  return (
    <div className="hw-full flex overflow-hidden" ref={ref}>
      {imageDetails.image ? <CanvasOnImage /> : <Placeholder />}
    </div>
  );
};

export default ImageHolder;
