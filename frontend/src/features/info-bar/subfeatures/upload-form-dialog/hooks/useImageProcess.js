import { useShallow } from "zustand/react/shallow";

import useImageStore from "@/store/image";
import { useImageDataMutation } from "@/features/info-bar/api/info-bar";

const useImageProcess = () => {
  const { setImage, setError } = useImageStore(
    useShallow((state) => ({
      setImage: state.setImage,
      setError: state.setError,
    })),
  );

  const { mutateAsync: processImage } = useImageDataMutation(setError);

  return { state: {}, action: { processImage, setImage } };
};

export default useImageProcess;
