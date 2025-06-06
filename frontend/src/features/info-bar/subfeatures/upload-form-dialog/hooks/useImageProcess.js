import { useShallow } from "zustand/react/shallow";

import useImageStore from "@/store/image";
import {
  useFetchColors,
  useImageDataMutation,
} from "@/features/info-bar/api/info-bar";

const useImageProcess = () => {
  const { setImage, setError } = useImageStore(
    useShallow((state) => ({
      setImage: state.setImage,
      setError: state.setError,
    })),
  );

  const { mutateAsync: processImage } = useImageDataMutation(setError);
  const { mutate: fetchColors } = useFetchColors(setError);

  return { state: {}, action: { fetchColors, processImage, setImage } };
};

export default useImageProcess;
