import React from "react";
import Button from "../../containers/common/Button";

function Login() {
  return (
    <div className="max-wscreen bg-gradient-135 flex h-screen max-h-screen w-screen items-center justify-center from-red-500 to-blue-500">
      <form className="flex h-[80%] w-[30%] flex-col items-center gap-16 rounded-3xl bg-white">
        <img
          className="mt-[15%] w-[45%]"
          src="assets/murata_logo.jpg"
          alt="Murata"
        />
        <div className="flex h-[7%] w-[60%] items-center bg-pink-300">
          <input
            className="h-full w-full rounded-xl bg-gray-300"
            type="text"
          ></input>
        </div>
        <div className="flex h-[7%] w-[60%] items-center bg-pink-300">
          <input
            className="h-full w-full rounded-xl bg-gray-300"
            type="text"
          ></input>
        </div>
        <div>
          <Button />
        </div>
      </form>
    </div>
  );
}

export default Login;
