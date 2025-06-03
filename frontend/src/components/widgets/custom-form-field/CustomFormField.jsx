import {
  FormControl,
  FormDescription,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/components/ui/popover";
import { cn } from "@/lib/utils";

import { cloneElement } from "react";

const CustomFormField = ({
  className,
  children,
  control,
  name,
  label,
  popoverTrigger,
}) => {
  return (
    <FormField
      name={name}
      control={control}
      render={({ field }) => (
        <FormItem className="flex-center hw-full flex-col p-2">
          <div className={cn("flex-center w-full", className)}>
            <FormLabel className="w-1/4">{label}</FormLabel>
            {popoverTrigger ? (
              <Popover>
                <PopoverTrigger>
                  <FormControl>
                    {cloneElement(popoverTrigger, { ...field })}
                  </FormControl>
                </PopoverTrigger>
                <PopoverContent>
                  {cloneElement(children, { ...field })}
                </PopoverContent>
              </Popover>
            ) : (
              <FormControl className="w-3/4">
                {cloneElement(children, { ...field })}
              </FormControl>
            )}
          </div>
          <FormDescription />
          <FormMessage className="flex-center" />
        </FormItem>
      )}
    />
  );
};

export default CustomFormField;
