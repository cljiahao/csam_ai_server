import { MARKERS } from "@/core/constants";
import { useColorStore } from "@/store/color";
import { useCoordStores } from "@/store/display";
import { useMarkerStore } from "@/store/marker";
import { useShallow } from "zustand/react/shallow";

const useMarking = () => {
  const colors = useColorStore((state) => state.colors);
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
    if (moveActive) return;
    const stored_mark = marks.find((mark) => mark.file_name === file_name);
    if (!stored_mark) {
      const firstColor = colors[0];
      addMark(file_name, {
        name: firstColor.defect_label,
        color: firstColor.hex_color,
        radius: 1,
      });
      return;
    }
    const currentColor = stored_mark.marker.color;
    const currentIndex = colors.findIndex(
      (c) => c.hex_color.toLowerCase() === currentColor.toLowerCase(),
    );
    if (currentIndex === colors.length - 1) {
      removeMark(file_name);
      removeMark(file_name + MARKERS.zoom.name, MARKERS.zoom);
      return;
    }
    const nextColor = colors[currentIndex + 1];
    updateMark(file_name, {
      name: nextColor.defect_label,
      color: nextColor.hex_color,
      radius: 1,
    });
    return;
  }

  return {
    state: { marks },
    action: { onMark, addMark, removeMark },
  };
};

export default useMarking;
