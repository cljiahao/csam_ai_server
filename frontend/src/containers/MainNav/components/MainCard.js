import React from "react";
import { Outlet, Link } from "react-router-dom";

const MainCard = ({ src, title, short, description, link }) => {
  return (
    <>
      <Link
        className="flex h-full w-full flex-col items-center gap-3 rounded-3xl bg-white shadow-2xl hover:scale-105 hover:bg-opacity-70"
        to={link}
        onClick={() => {
          window.location.href = link;
        }}
      >
        <div className="mb-5 mt-10 flex h-[20%] w-full items-center justify-center text-8xl 2xl:text-9xl">
          {src}
        </div>
        <h1 className="h-[15%] w-[80%] items-center break-words border-t-2 border-gray-300 text-center text-3xl font-bold tracking-wide 2xl:text-5xl">
          {title}
        </h1>
        <h3 className="text-xl 2xl:text-3xl">{short}</h3>
        <p className="mx-10 mb-10 mt-auto h-[20%] break-words text-justify 2xl:mx-20 2xl:mb-24 2xl:text-xl">
          {description}
        </p>
      </Link>
      <Outlet />
    </>
  );
};

export default MainCard;
