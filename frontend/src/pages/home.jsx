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
import { home_info } from "@/core/constants";

const Home = () => {
  return (
    <IconContext.Provider value={{ size: "6em" }}>
      <div className="flex-between h-screen gap-8 bg-amber-100 px-10 py-5">
        {home_info.map((card) => (
          <Link key={card.name} to={`/${card.name}`} className="hw-full">
            <Card className="flex-center hw-full hover:scale-105">
              <CardHeader className="flex-center hw-full gap-3 break-words tracking-wide">
                <CardContent className="flex-center hw-full py-16">
                  <card.icon />
                </CardContent>
                <CardTitle className="hw-full text-center text-4xl font-bold">
                  {card.title}
                </CardTitle>
                <CardDescription className="hw-full p-5 text-justify text-lg">
                  {card.description}
                </CardDescription>
              </CardHeader>
            </Card>
          </Link>
        ))}
        <Outlet />
      </div>
    </IconContext.Provider>
  );
};

export default Home;
