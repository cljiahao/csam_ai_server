import { MARKERS } from "@/core/constants";
import { useCoordStores } from "@/store/display";
import { useMarkerStore } from "@/store/marker";
import { useShallow } from "zustand/react/shallow";

const useMarking = () => {
  const { marks, addMark, updateMark, removeMark } = useMarkerStore(
    useShallow((state) => ({
      marks: state.marks,
      addMark: state.addMark,
      updateMark: state.updateMark,
      removeMark: state.removeMark,
    })),
  );
  const moveActive = useCoordStores((state) => state.moveActive);

  function onMark(e) {
    const file_name = e.currentTarget.id;
    if (!moveActive) {
      const stored_mark = marks.find((mark) => mark.file_name === file_name);
      if (!stored_mark) {
        addMark(file_name, MARKERS.colors[0]);
        return;
      }
      const last_marker = stored_mark.marker === MARKERS.colors.at(-1);
      if (last_marker) {
        removeMark(file_name);
        return;
      }
      updateMark(file_name, MARKERS.colors[stored_mark.marker.id]);
      return;
    }
  }

  return {
    state: { marks },
    action: { onMark, addMark, removeMark },
  };
};

export default useMarking;
