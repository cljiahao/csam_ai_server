import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import "./App.css";

import Main from "./pages/Main/Main";
import CDC from "./pages/CDC/CDC";
import CAI from "./pages/CAI/CAI";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Main />} />
        <Route path="/CDC" element={<CDC />} />
        <Route path="/CAI" element={<CAI />} />
      </Routes>
    </Router>
  );
}

export default App;
