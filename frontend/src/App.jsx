import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

import { CsamAI, CsamDC, Home } from "./pages";
import { navigation_info } from "./core/navigation";
import SeoHead from "./components/SeoHead";

const element_info = {
  home: <Home />,
  cdc: <CsamDC />,
  cai: <CsamAI />,
};

function App() {
  return (
    <Router>
      <Routes>
        {navigation_info.map((info) => (
          <Route
            key={info.name}
            path={info.url}
            element={
              <>
                <SeoHead title={info.title} />
                {element_info[info.name]}
              </>
            }
          />
        ))}
      </Routes>
    </Router>
  );
}

export default App;
