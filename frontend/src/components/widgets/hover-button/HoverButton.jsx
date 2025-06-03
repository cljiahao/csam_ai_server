import { createElement, forwardRef } from "react";

import { cn } from "@/lib/utils";
import { Button } from "@/components/ui/button";

const HoverButton = forwardRef(
  ({ className, icon, text, hoverText, ...props }, ref) => {
    return (
      <Button
        ref={ref}
        className={cn("flex-center group h-14 w-14", className)}
        {...props}
      >
        {(text || icon) && (
          <div className="flex-center w-full gap-2 group-hover:hidden">
            {icon && (
              <div className="group-hover:hidden">
                {createElement(icon, {
                  style: { width: "2rem", height: "2rem" },
                })}
              </div>
            )}
            {text && (
              <span className="text-wrap leading-tight group-hover:hidden">
                {text}
              </span>
            )}
          </div>
        )}
        <span
          className={`${(icon || text) && "hidden"} text-wrap leading-tight group-hover:block`}
        >
          {hoverText}
        </span>
      </Button>
    );
  },
);
HoverButton.displayName = "HoverButton";

export default HoverButton;
