import { useEffect } from "react";
import { useLocation } from "react-router-dom";
import { useIsMutating } from "@tanstack/react-query";

import { navigation_info } from "@/core/navigation";
import { useImageRef } from "./hooks/useImageRef";
import DotCanvas from "./components/DotCanvas";
import Loading from "@/components/status/loading";
import Error from "@/components/status/error";
import ImageHolder from "@/components/widgets/image_holder/ImageHolder";
import { usePanZoom } from "@/components/widgets/image_holder/hooks/usePanZoom";

const ImageDisplay = () => {
  const location = useLocation();
  const mode = location.pathname.split("/").pop();
  const title = navigation_info.find((nav) => nav.name == mode)?.title;
  const isMutating = useIsMutating({ mutationKey: ["imageProcess"] }); // For useMutation

  const {
    state: { moveActive },
  } = usePanZoom();

  const {
    state: { ref, imageRef, image, error },
    action: { setImageRef },
  } = useImageRef();

  useEffect(() => {
    if (ref.current) {
      setImageRef(ref);
    }
  }, [ref, imageRef, setImageRef]);

  return (
    <div className="hw-full flex overflow-hidden" ref={ref}>
      {error ? (
        <Error message={error} />
      ) : isMutating > 0 ? (
        <Loading />
      ) : (
        <ImageHolder image={image} placeholder_text={title}>
          <DotCanvas moveActive={moveActive} />
        </ImageHolder>
      )}
    </div>
  );
};

export default ImageDisplay;
