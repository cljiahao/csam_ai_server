import { useLocation } from "react-router-dom";

import { navigation_info } from "@/core/navigation";
import Error from "@/components/static/error";
import Loading from "@/components/static/loading";
import ImageHolder from "@/components/widgets/image-holder/ImageHolder";
import MarkCanvas from "@/components/widgets/mark-canvas/MarkCanvas";
import useImageDisplay from "./hooks/useImageDisplay";

const ImageDisplay = () => {
  const location = useLocation();
  const mode = location.pathname.split("/").pop();
  const title = navigation_info.find((nav) => nav.name == mode)?.title;

  const {
    state: {
      imageRef,
      markRef,
      error,
      image,
      marks,
      markColor,
      coordinates,
      isLoading,
    },
    action: { setMarks },
  } = useImageDisplay();

  return (
    <div className="hw-full flex overflow-hidden">
      <ImageHolder
        className="h-full"
        image={image}
        placeholder_text={title}
        ref={imageRef}
      >
        {error ? (
          <Error message={error} />
        ) : isLoading ? (
          <Loading />
        ) : (
          <MarkCanvas
            ref={markRef}
            canvasType="dot"
            marks={marks}
            setMarks={setMarks}
            markColor={markColor}
            coordinates={coordinates}
          />
        )}
      </ImageHolder>
    </div>
  );
};

export default ImageDisplay;
