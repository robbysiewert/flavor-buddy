import React, { Component } from 'react';
// import Form from './Form.js'; # remove later
import Selector from './Selector.js';

class App extends Component {
  render() {
    return (
      <div>
        <h1>What are you in the mood for today?</h1>
        <Selector />
      </div>
    );
  }
}

export default App;