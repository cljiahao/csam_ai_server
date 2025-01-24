import { Button } from "@/components/ui/button";

import useThumbnailHandlers from "../hooks/useThumbnailHandlers";

const Thumbnail = ({ directory, defect_mode, file_name }) => {
  const {
    state: { marksFileNames },
    action: { onFocus, unFocus, onMark },
  } = useThumbnailHandlers();

  const file_path = `/api/image/${directory}/${defect_mode}/${file_name}`;

  return (
    <Button
      id={file_name}
      className={`hw-full border-2 p-0 ${marksFileNames.has(file_name) ? "border-red-500" : ""}`}
      onMouseEnter={onFocus}
      onMouseLeave={unFocus}
      onClick={onMark}
    >
      <img src={file_path} alt={file_name} className="hw-full" />
    </Button>
  );
};

export default Thumbnail;
