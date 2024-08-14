// import Form from './Form.js'; # remove later
import React, { Component } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Selector from './Selector.js';
import SuggestionsPage from './SuggestionsPage.js';

class App extends Component {
  render() {
    return (
      <Router>
        <Routes>
          <Route path="/" element={<Selector />} />
          <Route path="/suggestions" element={<SuggestionsPage />} />
        </Routes>
      </Router>
    );
  }
}

export default App;

