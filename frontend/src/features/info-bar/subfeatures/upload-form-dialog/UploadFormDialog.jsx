import { Form } from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import CustomDialog from "@/components/widgets/custom-dialog/CustomDialog";
import CustomFormField from "@/components/widgets/custom-form-field/CustomFormField";
import HoverButton from "@/components/widgets/hover-button/HoverButton";
import useUploadFormDialog from "./hooks/useUploadFormDialog";

const UploadFormDialog = ({ triggerChildren, mode }) => {
  const {
    state: { isDialogOpen, ref, uploadFormInfo },
    action: { handleDialogOpen, uploadForm, onSubmit, onReset, onFileChange },
  } = useUploadFormDialog({ mode });

  return (
    <CustomDialog
      className="h-fit"
      trigger={triggerChildren}
      title={mode === "CDC" ? "Defects Collections" : "AI Predict Defects"}
      description="Upload image to start processing."
      open={isDialogOpen}
      onOpenChange={handleDialogOpen}
    >
      <Form {...uploadForm}>
        <form onSubmit={uploadForm.handleSubmit(onSubmit)}>
          {Object.keys(uploadFormInfo).map((key) => {
            const { label, placeholder, onBlur, disabled } =
              uploadFormInfo[key];
            return (
              <CustomFormField
                className="py-4"
                control={uploadForm.control}
                key={key}
                name={key}
                label={label}
              >
                <Input
                  placeholder={placeholder}
                  onBlur={onBlur}
                  disabled={disabled}
                />
              </CustomFormField>
            );
          })}
          <div className="flex-between pt-2">
            <HoverButton
              className="h-12 w-20"
              type="submit"
              hoverText="Upload"
            />
            <HoverButton
              className="h-12 w-20"
              hoverText="Reset"
              onClick={onReset}
            />
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
