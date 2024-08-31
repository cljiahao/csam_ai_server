import {
  useCanvasContext,
  useImageDetailsContext,
} from "@/contexts/csamContext";
import { useFetch } from "@/hooks/useFetch";
import { useInfoBarContext } from "@/modules/InfoBar/contexts/infoBarContext";
import { saveFinalJudgement } from "@/services/api_files";

const useSaveInput = () => {
  const { fetchData } = useFetch();
  const { marks } = useCanvasContext();
  const { imageDetails } = useImageDetailsContext();
  const { infoDetails } = useInfoBarContext();

  function createChipsDetails() {
    const chips = {};
    marks.forEach((mark) => {
      const category = mark.circle.name;
      if (mark.circle.radius == "1") {
        if (!chips[category]) chips[category] = [];
        chips[category].push(mark.id);
      }
    });

    return { chips: chips, directory: imageDetails.directory };
  }

  function saveUserInput({ mode }) {
    if (marks.length) {
      const chipsDetails = createChipsDetails();
      fetchData(
        saveFinalJudgement(
          chipsDetails,
          mode,
          infoDetails.lotNo,
          infoDetails.plate,
          infoDetails.item,
        ),
      );
    }
  }

  return saveUserInput;
};

export default useSaveInput;
