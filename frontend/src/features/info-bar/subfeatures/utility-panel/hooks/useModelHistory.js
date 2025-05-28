import { useState } from "react";
import {
  useFetchModelHistory,
  useQueryModelHistory,
} from "../api/fetchModelHistory";
import useBaseStore from "@/store/base";
import { useItemStore } from "@/features/info-bar/store/item";

const useModelHistory = () => {
  const [isDialogOpen, setDialogOpen] = useState();
  const updateError = useBaseStore((state) => state.updateError);
  const { mutateAsync: fetchModelHistory } = useFetchModelHistory({
    updateError,
  });
  const item = useItemStore((state) => state.item);
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
