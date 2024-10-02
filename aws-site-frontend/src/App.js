// import Form from './Form.js'; # remove later
import React, { Component } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Selector from './Selector.js';
import SuggestionsPage from './SuggestionsPage.js';
import WelcomePage from './WelcomePage';
import Navbar from './Navbar';
import About from './About.js';
import Contact from './Contact.js';


class App extends Component {
  render() {
    return (
      <Router>
      <Navbar />
        <Routes>
          <Route path="/" element={<WelcomePage />} />
          <Route path="/selector" element={<Selector />} />
          <Route path="/suggestions" element={<SuggestionsPage />} />
          <Route path="/about" element={<About />} />
          <Route path="/contact" element={<Contact />} />
        </Routes>
      </Router>
    );
  }
}

export default App;

