import {
  FormControl,
  FormDescription,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";

import { Input } from "@/components/ui/input";

const CustomFormField = ({
  control,
  name,
  label,
  placeholder,
  onBlur,
  disabled,
}) => {
  return (
    <FormField
      name={name}
      control={control}
      render={({ field }) => (
        <FormItem>
          <div className="flex-center">
            <FormLabel className="flex-end w-1/4 px-3">{label}</FormLabel>
            <FormControl className="flex w-3/4 px-3">
              <Input
                {...field}
                placeholder={placeholder}
                value={field.value}
                onBlur={onBlur}
                disabled={disabled}
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

export default CustomFormField;
