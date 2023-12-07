import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import "./App.css";

import Main from "./pages/Main/Main";
import CDC from "./pages/CDC/CDC";
import CAI from "./pages/CAI/CAI";
import Settings from "./pages/Settings/Settings";
import Login from "./pages/Login/Login";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Main />} />
        <Route path="CDC" element={<CDC />} />
        <Route path="CAI" element={<CAI />} />
        <Route path="Settings" element={<Settings />} />
        <Route path="Login" element={<Login />} />
      </Routes>
    </Router>
  );
}

export default App;
