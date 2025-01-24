import { createElement, forwardRef } from "react";

import { cn } from "@/lib/utils";
import { Button } from "@/components/ui/button";

const HoverButton = forwardRef(({ className, icon, text, ...props }, ref) => {
  return (
    <Button
      ref={ref}
      className={cn("flex-center group h-14 w-14", className)}
      {...props}
    >
      {icon && (
        <div className="group-hover:hidden">
          {createElement(icon, { style: { width: "2rem", height: "2rem" } })}
        </div>
      )}
      <span
        className={`${icon && "hidden"} text-wrap text-sm group-hover:block`}
      >
        {text}
      </span>
    </Button>
  );
});

HoverButton.displayName = "HoverButton";

export default HoverButton;
