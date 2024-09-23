import {
  FormControl,
  FormDescription,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import { Input } from "@/components/ui/input";

const ImageFormCard = ({ form, name, label, value, placeholder, onBlur }) => {
  return (
    <FormField
      control={form.control}
      name={name}
      render={({ field }) => (
        <FormItem>
          <div className="flex-center">
            <FormLabel className="flex-end w-1/4 px-3">{label}</FormLabel>
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
};

export default ImageFormCard;
