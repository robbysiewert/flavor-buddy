import React, { Component } from 'react';
// import Form from './Form.js';
import Selector from './Selector.js';

class App extends Component {
  render() {
    return (
      <div>
        <h1>Select an option:</h1>
        <Selector />
      </div>
    );
  }
}

export default App;