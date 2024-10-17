import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import LandingPage from "./components/Landingpage"; // Update the path
import Retouching from "./components/Retouching"; // Update the path

function App() {
  return (
    <Router>
      <Routes>
      <Route path="/" element={<LandingPage />} />
        <Route path="/upload" element={<Retouching />} />
      </Routes>
    </Router>
  );
}

export default App;



