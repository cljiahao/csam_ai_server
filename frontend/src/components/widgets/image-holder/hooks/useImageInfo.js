import { useCallback } from "react";
import { useEffect } from "react";
import { useRef, useState } from "react";

const useImageInfo = () => {
  const imageRef = useRef(null);
  const [imageSize, setImagesize] = useState({ width: 0, height: 0 });

  const getImageBoundingRect = () => {
    if (imageRef.current) {
      return imageRef.current.getBoundingClientRect();
    }
    return null;
  };

  const handleImageLoad = useCallback(() => {
    const containerRect = getImageBoundingRect();
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
  }, []);

  // Update rect when window resizes
  useEffect(() => {
    window.addEventListener("resize", handleImageLoad);
    return () => window.removeEventListener("resize", handleImageLoad);
  }, [handleImageLoad]);

  return {
    state: { imageRef, imageSize },
    action: { handleImageLoad },
  };
};

export default useImageInfo;
