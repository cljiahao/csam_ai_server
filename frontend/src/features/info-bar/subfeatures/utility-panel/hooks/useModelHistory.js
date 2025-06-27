import { useState } from "react";

import useBaseStore from "@/store/base";
import {
  useFetchModelHistory,
  useQueryModelHistory,
} from "@/features/info-bar/api/info-bar";
import { useInfoBarContext } from "@/features/info-bar/contexts/InfoBarContext";

const useModelHistory = () => {
  const [isDialogOpen, setDialogOpen] = useState();
  const { item } = useInfoBarContext();
  const updateError = useBaseStore((state) => state.updateError);

  const { mutateAsync: fetchModelHistory } = useFetchModelHistory(updateError);
  const modelHistoryByItem = useQueryModelHistory(item);
  const allModelHistory = useQueryModelHistory("");

  const handleDialogOpen = () => {
    if (!isDialogOpen) {
      fetchModelHistory({ item: "" });
    }
    setDialogOpen((prevState) => !prevState);
  };

  return {
    state: { isDialogOpen, allModelHistory, modelHistoryByItem },
    action: { handleDialogOpen, fetchModelHistory },
  };
};

export default useModelHistory;
