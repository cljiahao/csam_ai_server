import { useEffect } from "react";
import { useRef, useState } from "react";

const useImageInfo = () => {
  const imageRef = useRef(null);
  const [imageSize, setImagesize] = useState({ width: 0, height: 0 });

  // Update rect when window resizes
  useEffect(() => {
    window.addEventListener("resize", handleImageLoad);
    return () => window.removeEventListener("resize", handleImageLoad);
  }, []);

  const handleImageLoad = () => {
    const containerRect = imageRef.current?.getBoundingClientRect();
    const imageAspectRatio =
      imageRef.current.naturalWidth / imageRef.current.naturalHeight;

    const containerWidth = containerRect.width;
    const containerHeight = containerRect.height;
    const containerAspectRatio = containerWidth / containerHeight;

    if (imageAspectRatio > containerAspectRatio) {
      setImagesize({
        width: Math.round(containerWidth),
        height: Math.round(containerWidth / imageAspectRatio),
      });
    } else {
      setImagesize({
        width: Math.round(containerHeight * imageAspectRatio),
        height: Math.round(containerHeight),
      });
    }
  };

  return {
    state: { imageRef, imageSize },
    action: { handleImageLoad },
  };
};

export default useImageInfo;
