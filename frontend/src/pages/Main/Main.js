import React from "react";
import "./Main.css";
import MainNav from "../../containers/MainNav/MainNav";

function Main() {
  return (
    <div className="flex h-screen w-screen items-center justify-center bg-amber-50">
      <MainNav />
    </div>
  );
}

export default Main;
