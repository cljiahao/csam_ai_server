import { Link } from "react-router-dom";
import { Outlet } from "react-router-dom";
import { IconContext } from "react-icons";

import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { navigation_info } from "@/core/navigation";

const Home = () => {
  return (
    <IconContext.Provider value={{ size: "6em" }}>
      <div className="flex-between h-screen gap-10 bg-amber-200/50 px-12 py-7">
        {navigation_info
          .filter((info) => info.name.toLowerCase() !== "home")
          .map((info) => (
            <Link key={info.name} to={info.url} className="hw-full">
              <Card className="flex-center hw-full hover: bg-white hover:scale-105 hover:bg-slate-50">
                <CardHeader className="flex-center hw-full gap-3 break-words tracking-wide">
                  <CardContent className="flex-center hw-full py-16">
                    <info.icon />
                  </CardContent>
                  <CardTitle className="hw-full text-center text-4xl font-bold">
                    {info.title}
                  </CardTitle>
                  <CardDescription className="hw-full p-5 text-justify text-lg">
                    {info.description}
                  </CardDescription>
                </CardHeader>
              </Card>
            </Link>
          ))}
        <Outlet />
        <div className="absolute bottom-0 right-3 text-xs">
          <p>App Version: {import.meta.env.VITE_APP_VERSION}</p>
        </div>
      </div>
    </IconContext.Provider>
  );
};

export default Home;
