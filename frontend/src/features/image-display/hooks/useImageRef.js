import { useImageStore } from "@/store/display";
import { useRef } from "react";
import { useShallow } from "zustand/react/shallow";

export const useImageRef = () => {
  const ref = useRef(null);

  const { imageRef, image, error, setImageRef, setImage } = useImageStore(
    useShallow((state) => ({
      imageRef: state.imageRef,
      image: state.image,
      error: state.error,
      setImageRef: state.setImageRef,
      setImage: state.setImage,
    })),
  );

  return {
    state: { ref, imageRef, image, error },
    action: { setImageRef, setImage },
  };
};
