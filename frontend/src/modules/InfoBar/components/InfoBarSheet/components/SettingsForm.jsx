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
import useSettingsForm from "../hooks/useSettingsForm";
import HoverButton from "@/components/HoverButton";
import { Separator } from "@/components/ui/separator";

const SettingsForm = ({ page }) => {
  const [form_info, form] = useSettingsForm(page);

  // Submit form data and trigger file input
  const onSubmit = useCallback((onSubmitData) => {
    console.log(onSubmitData);
  }, []);

  // Handle form reset
  const onReset = useCallback(() => {
    form.reset();
  }, [form]);

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
        {Object.keys(form_info).map((key) => {
          const { label } = form_info[key];
          const fileRef = form.register(key);
          return (
            <FormField
              key={key}
              control={form.control}
              name={key}
              render={() => (
                <FormItem>
                  <div className="flex-start flex-col space-y-2">
                    <FormLabel className="flex w-full flex-col px-3 py-2 text-base">
                      {label}
                      <Separator className="my-2 pt-[2px]" />
                    </FormLabel>
                    <FormControl className="flex-center px-3">
                      <Input type="file" {...fileRef} />
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

export default SettingsForm;
