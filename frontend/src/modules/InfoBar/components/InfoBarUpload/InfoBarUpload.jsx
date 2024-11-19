import { useCallback, useRef, useState } from "react";

import { useImageDetailsContext } from "@/contexts/context";
import { navigation_info } from "@/core/navigation";
import { Input } from "@/components/ui/input";
import { toast } from "@/components/ui/use-toast";
import DialogPopUp from "@/components/DialogPopUp";
import HoverButton from "@/components/HoverButton";
import { useInfoBarContext } from "../../contexts/infoBarContext";
import useLoadImage from "./hooks/useLoadImage";
import ImageForm from "./components/ImageForm";

const InfoBarUpload = ({ page }) => {
  const { updateImageDetails } = useImageDetailsContext();
  const { infoDetails } = useInfoBarContext();
  const getProcessedImage = useLoadImage();
  const fileInputRef = useRef(null);
  const [isOpen, setIsOpen] = useState(false);

  // Handle file input change
  const onFileChange = useCallback(
    (event) => {
      event.preventDefault();
      setIsOpen(false);

      const file = event.target.files[0];
      if (file) {
        toast({
          title: "You submitted the following values:",
          description: (
            <pre className="mt-2 flex w-[340px] flex-col rounded-md bg-slate-950 p-4">
              <kbd className="text-white">File Name: {file.name}</kbd>
              <kbd className="text-white">Item: {infoDetails.item}</kbd>
            </pre>
          ),
          duration: 2000,
        });
        // Reset and update imageDetails with new file
        updateImageDetails({
          image: file,
          chips: null,
          directory: "",
          detail: "",
          isLoading: true,
        });
        // Send uploaded file to process
        getProcessedImage(page, file, infoDetails);
      }
    },
    [infoDetails, updateImageDetails, getProcessedImage, page],
  );

  // Dialog configuration
  const dialog_info = {
    trigger: (
      <HoverButton
        className="h-14 w-14 text-3xl"
        TriggerIcon={
          navigation_info.find((item) => item.name === page.toUpperCase())?.icon
        }
      >
        <div className="flex flex-col text-sm">
          <span>{page}</span>
          <span>Upload</span>
        </div>
      </HoverButton>
    ),
    title: page === "CDC" ? "Defects Collections" : "AI Predict Defects",
    description: "Upload image to start processing.",
  };

  return (
    <DialogPopUp
      trigger={dialog_info.trigger}
      title={dialog_info.title}
      description={dialog_info.description}
      open={isOpen}
      onOpenChange={setIsOpen}
    >
      <ImageForm page={page} fileInputRef={fileInputRef} />
      <Input
        className="hidden"
        type="file"
        accept=".png, .jpg"
        ref={fileInputRef}
        onChange={onFileChange}
      />
    </DialogPopUp>
  );
};

export default InfoBarUpload;
