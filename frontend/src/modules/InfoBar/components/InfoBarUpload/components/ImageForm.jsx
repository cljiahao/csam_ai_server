import { useCallback } from "react";
import {
  Form,
  FormControl,
  FormDescription,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import HoverButton from "@/components/HoverButton";
import useImageForm from "../hooks/useImageForm";
import { useInfoBarContext } from "@/modules/InfoBar/contexts/infoBarContext";

const ImageForm = ({ page, fileInputRef }) => {
  const [form_info, form] = useImageForm(page);
  const { updateInfoDetails } = useInfoBarContext();

  // Submit form data and trigger file input
  const onSubmit = useCallback(
    (onSubmitData) => {
      updateInfoDetails(onSubmitData);
      fileInputRef.current?.click();
    },
    [fileInputRef, updateInfoDetails],
  );

  // Handle form reset
  const onReset = useCallback(() => {
    form.reset();
    updateInfoDetails({ item: "" });
  }, [form, updateInfoDetails]);

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-8">
        {Object.keys(form_info).map((key) => {
          const { label, value, placeholder, onBlur } = form_info[key];
          return (
            <FormField
              key={key}
              control={form.control}
              name={key}
              render={({ field }) => (
                <FormItem>
                  <div className="flex-center">
                    <FormLabel className="flex-end w-1/4 px-3">
                      {label}
                    </FormLabel>
                    <FormControl className="flex w-3/4 px-3">
                      <Input
                        {...field}
                        value={value || field.value || ""}
                        placeholder={placeholder}
                        onBlur={onBlur}
                        disabled={!!value}
                      />
                    </FormControl>
                  </div>
                  <FormDescription />
                  <FormMessage className="flex-center" />
                </FormItem>
              )}
            />
          );
        })}
        <div className="flex-between">
          <HoverButton type="submit">Upload</HoverButton>
          <HoverButton onClick={onReset}>Reset</HoverButton>
        </div>
      </form>
    </Form>
  );
};

export default ImageForm;
