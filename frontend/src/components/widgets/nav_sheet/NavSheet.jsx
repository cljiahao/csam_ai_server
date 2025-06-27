import { IconContext } from "react-icons";
import { IoMenu } from "react-icons/io5";

import { Sheet, SheetContent, SheetTrigger } from "@/components/ui/sheet";
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
      <SheetContent className="flex h-full w-full flex-col py-2">
        <NavMenu nav_info={nav_info} />
        <Separator />
        <div className="flex min-h-0 flex-1">{children}</div>
      </SheetContent>
    </Sheet>
  );
};

export default NavSheet;
