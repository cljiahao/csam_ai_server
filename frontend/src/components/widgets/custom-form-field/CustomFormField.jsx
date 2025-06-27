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
      render={({ field }) => {
        const createMergedProps = (originalElement, fieldProps) => {
          const merged = { ...fieldProps };
          if (!originalElement) {
            return merged;
          }
          const originalProps = originalElement.props;

          for (const key in originalProps) {
            if (Object.prototype.hasOwnProperty.call(originalProps, key)) {
              const originalValue = originalProps[key];
              const fieldValue = fieldProps[key];
              if (
                typeof originalValue === "function" &&
                typeof fieldValue === "function"
              )
                merged[key] = (...args) => {
                  originalValue(...args);
                  fieldValue(...args);
                };
            }
          }
          return merged;
        };

        const childrenMergedProps = createMergedProps(children, field);
        let popoverTriggerMergedProps = {};
        if (popoverTrigger) {
          popoverTriggerMergedProps = createMergedProps(popoverTrigger, field);
        }

        return (
          <FormItem className="flex-center hw-full flex-col space-y-0">
            <div className={cn("flex-center w-full", className)}>
              {label && <FormLabel className="w-1/4">{label}</FormLabel>}
              {popoverTrigger ? (
                <Popover>
                  <PopoverTrigger>
                    <FormControl>
                      {cloneElement(popoverTrigger, popoverTriggerMergedProps)}
                    </FormControl>
                  </PopoverTrigger>
                  <PopoverContent>
                    {cloneElement(children, childrenMergedProps)}
                  </PopoverContent>
                </Popover>
              ) : (
                <FormControl className="w-3/4">
                  {cloneElement(children, childrenMergedProps)}
                </FormControl>
              )}
            </div>
            <FormDescription />
            <FormMessage className="flex-center" />
          </FormItem>
        );
      }}
    />
  );
};

export default CustomFormField;
