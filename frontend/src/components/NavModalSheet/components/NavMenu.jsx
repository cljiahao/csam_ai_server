import { Link } from "react-router-dom";
import { Outlet } from "react-router-dom";
import { IconContext } from "react-icons";

import {
  NavigationMenu,
  NavigationMenuItem,
  NavigationMenuList,
  navigationMenuTriggerStyle,
} from "@/components/ui/navigation-menu";

// TODO: Update the navigation menu link css (width) to dynamically
//       change based on the number of nav_info elements

const NavMenu = ({ nav_info }) => {
  return (
    <IconContext.Provider value={{ size: "3em" }}>
      <div className="flex-center h-14 w-full">
        <NavigationMenu>
          <NavigationMenuList>
            {nav_info.map((nav) => (
              <NavigationMenuItem key={nav.name}>
                <Link
                  to={nav.url}
                  className={`${navigationMenuTriggerStyle()} h-full`}
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
