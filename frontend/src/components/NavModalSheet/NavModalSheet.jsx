import { IconContext } from "react-icons";
import { IoMenu } from "react-icons/io5";

import { navigation_info } from "@/core/navigation";
import {
  Sheet,
  SheetContent,
  SheetDescription,
  SheetHeader,
  SheetTitle,
  SheetTrigger,
} from "@/components/ui/sheet";
import { Separator } from "@/components/ui/separator";
import NavMenu from "./components/NavMenu";

const NavModalSheet = ({ children, ...props }) => {
  return (
    <IconContext.Provider value={{ size: "2.5em" }}>
      <Sheet {...props}>
        <SheetTrigger>
          <IoMenu />
        </SheetTrigger>
        <SheetContent className="py-2">
          <SheetHeader>
            <SheetTitle>
              <SheetDescription />
            </SheetTitle>
          </SheetHeader>
          <NavMenu nav_info={navigation_info} />
          <Separator className="my-2" />
          {children}
        </SheetContent>
      </Sheet>
    </IconContext.Provider>
  );
};

export default NavModalSheet;
