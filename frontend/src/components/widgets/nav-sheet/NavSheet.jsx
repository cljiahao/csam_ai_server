import { IconContext } from "react-icons";
import { IoMenu } from "react-icons/io5";

import {
  Sheet,
  SheetContent,
  SheetDescription,
  SheetHeader,
  SheetTitle,
  SheetTrigger,
} from "@/components/ui/sheet";
import { Separator } from "@/components/ui/separator";
import NavMenu from "@/components/widgets/nav-sheet/components/NavMenu";

const NavSheet = ({ children, nav_info, ...props }) => {
  return (
    <Sheet {...props}>
      <SheetTrigger>
        <IconContext.Provider value={{ size: "2.5em" }}>
          <IoMenu />
        </IconContext.Provider>
      </SheetTrigger>
      <SheetContent className="hw-full flex flex-col gap-0 py-0">
        <SheetHeader className="flex-center w-full py-2">
          <SheetTitle className="sr-only" />
          <SheetDescription className="sr-only" />
          <NavMenu nav_info={nav_info} />
          <Separator />
        </SheetHeader>
        <div className="flex min-h-0 flex-1">{children}</div>
      </SheetContent>
    </Sheet>
  );
};

export default NavSheet;
