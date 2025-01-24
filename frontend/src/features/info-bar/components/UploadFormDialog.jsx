import { useLocation } from "react-router-dom";

import { Form } from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import CustomDialog from "@/components/widgets/custom_dialog/CustomDialog";
import HoverButton from "@/components/widgets/hover_button/HoverButton";
import CustomFormField from "@/components/widgets/custom_form_field/CustomFormField";
import { navigation_info } from "@/core/navigation";
import useFormValidation from "../hooks/useFormValidation";
import useImageProcess from "../hooks/useImageProcess";
import { useQueryClient } from "@tanstack/react-query";
import { resetStore } from "@/store/resetStore";
import { toast } from "@/hooks/use-toast";
import useSaveUserInput from "../hooks/useSaveUserInput";

const UploadFormDialog = ({ setLotNo, setPlateNo }) => {
  const location = useLocation();
  const mode = location.pathname.split("/").pop();
  const nav = navigation_info.find((nav) => nav.name === mode);
  const queryClient = useQueryClient();
  const {
    state: { ref, uploadFormInfo },
    action: { onSubmit, onReset, uploadForm },
  } = useFormValidation();

  const {
    state: { isDialogOpen },
    action: { setDialogOpen, handleImageProcess },
  } = useImageProcess();

  const {
    action: { handleSaveUserInput },
  } = useSaveUserInput();

  const handleDialogOpen = () => {
    if (!isDialogOpen) {
      handleSaveUserInput();
    }

    setDialogOpen((prevState) => !prevState);
  };

  const onFileChange = (e) => {
    e.preventDefault();

    const file = e.target.files[0];
    if (file) {
      queryClient.removeQueries();
      resetStore();

      const item = uploadForm.getValues("item");
      const lotNo = uploadForm.getValues("lotNo");

      setDialogOpen(false);
      setLotNo(lotNo);
      setPlateNo(file.name.split(".")[0]);

      toast({
        title: "You submitted the following values:",
        description: (
          <pre className="mt-2 flex w-[340px] flex-col rounded-md bg-slate-950 p-4">
            <kbd className="text-white">Lot No: {lotNo}</kbd>
            <kbd className="text-white">File Name: {file.name}</kbd>
            <kbd className="text-white">Item: {item}</kbd>
          </pre>
        ),
        duration: 2000,
      });

      handleImageProcess(mode, item, lotNo, file);
    }
  };

  return (
    <CustomDialog
      trigger={<HoverButton icon={nav.icon} text={`${nav.name} Upload`} />}
      title={mode === "CDC" ? "Defects Collections" : "AI Predict Defects"}
      description="Upload image to start processing."
      open={isDialogOpen}
      onOpenChange={handleDialogOpen}
    >
      <Form {...uploadForm}>
        <form
          onSubmit={uploadForm.handleSubmit(onSubmit)}
          className="space-y-8 pt-4"
        >
          {Object.keys(uploadFormInfo).map((key) => {
            const { label, placeholder, onBlur, disabled } =
              uploadFormInfo[key];
            return (
              <CustomFormField
                control={uploadForm.control}
                key={key}
                name={key}
                label={label}
                placeholder={placeholder}
                onBlur={onBlur}
                disabled={disabled}
              />
            );
          })}
          <div className="flex-between flex">
            <HoverButton className="h-12 w-20" type="submit" text="Upload" />
            <HoverButton className="h-12 w-20" text="Reset" onClick={onReset} />
          </div>
        </form>
      </Form>
      <Input
        className="hidden"
        type="file"
        accept=".png, .jpg"
        ref={ref}
        onChange={onFileChange}
      />
    </CustomDialog>
  );
};

export default UploadFormDialog;
