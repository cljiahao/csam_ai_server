import { createElement } from "react";
import { Link } from "react-router-dom";
import { Outlet } from "react-router-dom";
import { IconContext } from "react-icons";

import { navigation_info } from "@/core/navigation";
import MediaCard from "@/components/widgets/media-card/MediaCard";

const Home = () => {
  return (
    <IconContext.Provider value={{ size: "6em" }}>
      <div className="flex-between h-screen gap-10 bg-amber-200/50 px-12 py-7">
        {navigation_info
          .filter((nav) => nav.name.toLowerCase() !== "home")
          .map((nav) => (
            <Link key={nav.name} to={nav.url} className="hw-full">
              <MediaCard
                className="hover: space-y-20 bg-white text-4xl hover:scale-105 hover:bg-slate-50"
                title={nav.title}
                description={nav.description}
                descClassName="pt-6 text-lg w-[75%] text-center"
              >
                <div className="text-xl">{createElement(nav.icon)}</div>
              </MediaCard>
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
