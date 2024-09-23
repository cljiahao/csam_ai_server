import { forwardRef } from "react";
import { Button } from "./ui/button";

const HoverButton = forwardRef(
  ({ children, className, TriggerIcon, ...props }, ref) => {
    return (
      <Button ref={ref} className={className} {...props}>
        {TriggerIcon ? (
          <div className="flex-center group gap-3">
            <TriggerIcon className="group-hover:hidden" />
            <span className="hidden text-lg group-hover:block">{children}</span>
          </div>
        ) : (
          children
        )}
      </Button>
    );
  },
);

HoverButton.displayName = "HoverButton";

export default HoverButton;
