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
import NavMenu from "@/components/widgets/nav_sheet/components/NavMenu";

const NavSheet = ({ children, nav_info, ...props }) => {
  return (
    <Sheet {...props}>
      <SheetTrigger>
        <IconContext.Provider value={{ size: "2.5em" }}>
          <IoMenu />
        </IconContext.Provider>
      </SheetTrigger>
      <SheetContent className="py-2">
        <SheetHeader>
          <SheetTitle>
            <SheetDescription />
          </SheetTitle>
        </SheetHeader>
        <NavMenu nav_info={nav_info} />
        <Separator className="my-2" />
        {children}
      </SheetContent>
    </Sheet>
  );
};

export default NavSheet;
