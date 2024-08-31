import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

import Home from "./pages/home";
import CsamDC from "./pages/csamdc";
import CsamAI from "./pages/csamai";
import Settings from "./pages/settings";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/CDC" element={<CsamDC />} />
        <Route path="/CAI" element={<CsamAI />} />
        <Route path="/config" element={<Settings />} />
      </Routes>
    </Router>
  );
}

export default App;
