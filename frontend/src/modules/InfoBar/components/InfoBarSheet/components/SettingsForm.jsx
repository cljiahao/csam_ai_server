import {
  Form,
  FormControl,
  FormDescription,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import useSettingsForm from "../hooks/useSettingsForm";

const SettingsForm = () => {
  const [form_info, form] = useSettingsForm();
  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-8"></form>
    </Form>
  );
};

export default SettingsForm;
