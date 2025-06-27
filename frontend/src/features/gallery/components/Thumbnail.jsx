import { Button } from "@/components/ui/button";

import useThumbnailHandlers from "../hooks/useThumbnailHandlers";

const Thumbnail = ({ id, directory, defect_mode, file_name }) => {
  const {
    state: { marksID },
    action: { onFocus, unFocus, onClick },
  } = useThumbnailHandlers();

  // TODO: use getImageSrc instead of directly using filepath
  const file_path = `/api/csam_image/${directory}/${defect_mode}/${file_name}`;

  return (
    <Button
      id={id}
      className={`hw-full border-2 p-0 ${marksID.has(id) ? "border-red-500" : ""}`}
      onMouseEnter={onFocus}
      onMouseLeave={unFocus}
      onClick={onClick}
    >
      <img src={file_path} alt={file_name} className="hw-full" />
    </Button>
  );
};

export default Thumbnail;
