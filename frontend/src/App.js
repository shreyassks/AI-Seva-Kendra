import "./App.css";
import Home from "./Home/Home";
import Dashboard from "./Dashboard/Dashboard";
import Conversation from "./Conversation/Conversation";

import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

function App() {
  return (
    <Router>
      <div className="App">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/dashboard" exact element={<Dashboard />} />
          <Route path="/conversation" element={<Conversation />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
