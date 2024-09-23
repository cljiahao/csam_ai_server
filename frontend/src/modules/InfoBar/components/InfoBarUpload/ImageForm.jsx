import { useCallback, useRef, useState } from "react";

import { useImageDetailsContext } from "@/contexts/context";
import { navigation_info } from "@/core/navigation";
import { Form } from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import { toast } from "@/components/ui/use-toast";
import DialogPopUp from "@/components/DialogPopUp/DialogPopUp";
import HoverButton from "@/components/HoverButton";
import { useInfoBarContext } from "../../contexts/infoBarContext";
import ImageFormButton from "./components/ImageFormButton/ImageFormButton";
import ImageFormCard from "./components/ImageFormCard";
import useImageForm from "./hooks/useImageForm";
import useLoadImage from "./hooks/useLoadImage";
import useSaveInput from "./hooks/useSaveInput";

const InfoBarUpload = ({ mode }) => {
  const { updateImageDetails } = useImageDetailsContext();
  const { infoDetails, updateInfoDetails } = useInfoBarContext();
  const [form_info, form] = useImageForm();
  const getProcessedImage = useLoadImage();
  const saveUserInput = useSaveInput();
  const fileInputRef = useRef(null);
  const [isOpen, setIsOpen] = useState(false);

  // Submit form data and trigger file input
  const onSubmit = useCallback(
    (onSubmitData) => {
      saveUserInput({ mode });
      updateInfoDetails(onSubmitData);
      fileInputRef.current?.click();
    },
    [mode, saveUserInput, updateInfoDetails],
  );

  // Handle file input change
  const onFileChange = useCallback(
    (event) => {
      event.preventDefault();
      setIsOpen(false);

      const file = event.target.files[0];
      if (file) {
        toast({
          title: "You submitted the following values:",
          description: infoDetails.item,
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
        getProcessedImage(mode, file, infoDetails);
      }
    },
    [infoDetails, updateImageDetails, mode, getProcessedImage],
  );

  // Dialog configuration
  const dialog_info = {
    trigger: (
      <HoverButton
        className="h-14 w-14 text-3xl"
        TriggerIcon={
          navigation_info.find((item) => item.name === mode.toUpperCase())?.icon
        }
      >
        <div className="flex flex-col text-sm">
          <span>{mode}</span>
          <span>Upload</span>
        </div>
      </HoverButton>
    ),
    title: "AI Predict Defects",
    description: "Upload image to start processing.",
  };

  return (
    <DialogPopUp
      trigger={dialog_info.trigger}
      title={dialog_info.title}
      descr={dialog_info.description}
      open={isOpen}
      onOpenChange={setIsOpen}
    >
      <Form {...form}>
        <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-8">
          {Object.keys(form_info).map((key) => {
            const { label, value, placeholder, onBlur } = form_info[key];
            return (
              <ImageFormCard
                key={key}
                form={form}
                name={key}
                label={label}
                value={value}
                placeholder={placeholder}
                onBlur={onBlur}
              />
            );
          })}
          <ImageFormButton form={form} />
        </form>
      </Form>
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
