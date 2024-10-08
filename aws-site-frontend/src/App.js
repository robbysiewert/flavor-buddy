// import Form from './Form.js'; # remove later
import React, { Component } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Selector from './Selector.js';
import SuggestionsPage from './SuggestionsPage.js';
import WelcomeFlavor from './WelcomeFlavor.js';
import Navbar from './Navbar';
import About from './About.js';
import ToolOrLearn from './ToolOrLearn.js';


class App extends Component {
  render() {
    return (
      <Router>
      <Navbar />
        <Routes>
          <Route path="/" element={<ToolOrLearn />} />
          <Route path="/welcome-flavor" element={< WelcomeFlavor/>} />
          <Route path="/selector" element={<Selector />} />
          <Route path="/suggestions" element={<SuggestionsPage />} />
          <Route path="/about" element={<About />} />
        </Routes>
      </Router>
    );
  }
}

export default App;

