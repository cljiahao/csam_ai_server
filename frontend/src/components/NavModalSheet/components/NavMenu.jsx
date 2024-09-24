import { Link } from "react-router-dom";
import { Outlet } from "react-router-dom";
import { IconContext } from "react-icons";

import {
  NavigationMenu,
  NavigationMenuItem,
  NavigationMenuList,
  navigationMenuTriggerStyle,
} from "@/components/ui/navigation-menu";

const NavMenu = ({ nav_info }) => {
  const nav_len = nav_info.length;
  const width = nav_len === 3 ? "px-7" : nav_len === 4 ? "px-4" : "";
  return (
    <IconContext.Provider value={{ size: "3em" }}>
      <div className="flex-center h-14 w-full">
        <NavigationMenu>
          <NavigationMenuList>
            {nav_info.map((nav) => (
              <NavigationMenuItem key={nav.name}>
                <Link
                  to={nav.url}
                  className={`${navigationMenuTriggerStyle()} h-full ${width}`}
                >
                  <nav.icon />
                </Link>
              </NavigationMenuItem>
            ))}
          </NavigationMenuList>
          <Outlet />
        </NavigationMenu>
      </div>
    </IconContext.Provider>
  );
};

export default NavMenu;
