import React from 'react';
import { BrowserRouter as Router, Routes, Route, useLocation } from 'react-router-dom';
import Selector from './Selector';
import SuggestionsPage from './SuggestionsPage';
import WelcomeFlavor from './WelcomeFlavor';
import Navbar from './Navbar';
import About from './About';
import ToolOrLearn from './ToolOrLearn';

function App() {
  const location = useLocation();

  return (
    <>
      {location.pathname !== '/' && <Navbar />}
      <Routes>
        <Route path="/" element={<ToolOrLearn />} />
        <Route path="/welcome-flavor" element={<WelcomeFlavor />} />
        <Route path="/selector" element={<Selector />} />
        <Route path="/suggestions" element={<SuggestionsPage />} />
        <Route path="/about" element={<About />} />
      </Routes>
    </>
  );
}

export default function AppWrapper() {
  return (
    <Router>
      <App />
    </Router>
  );
}
