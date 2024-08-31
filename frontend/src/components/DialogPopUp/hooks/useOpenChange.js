import { useCallback, useState } from "react";

export const useOpenChange = (callback) => {
  const [isOpen, setIsOpen] = useState(false);

  const onOpenChange = useCallback(
    (open) => {
      setIsOpen(open);
      callback(open);
    },
    [callback],
  );
  return [isOpen, onOpenChange];
};
