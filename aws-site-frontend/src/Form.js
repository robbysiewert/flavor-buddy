import React, { Component } from 'react';
import axios from 'axios';

// Define the API Gateway URL as a constant
const apiUrl = process.env.REACT_APP_API_GATEWAY_URL;
// const apiUrl = 'https://741vgm2996.execute-api.us-west-2.amazonaws.com/prod/';

export default class Form extends Component {
  constructor(props) {
    super(props);
    this.state = {
      name: '',
      message: '',
      response: '', // New state to hold the formatted response
    };
    this.handleSubmit = this.handleSubmit.bind(this);
    this.handleChange = this.handleChange.bind(this);
  }

  handleChange(event) {
    const inputValue = event.target.value;
    const stateField = event.target.name;
    this.setState({
      [stateField]: inputValue,
    });
    console.log(this.state);
  }

  async handleSubmit(event) {
    event.preventDefault();
    const { name, message } = this.state;
    console.log(apiUrl)

    // Post data to Lambda function
    await axios.post(
      `${apiUrl}/storage`,
      {
        identifier: name,
        attribute1: message,
      }
    );

    // Fetch data from Lambda function using GET method
    try {
      const response = await axios.get(
        `${apiUrl}/storage`,
        {
          params: {
            identifier: name,
          },
        }
      );

      // Extract values from the response object
      const { identifier, Attribute1 } = response.data;
      this.setState({
        response: {
          identifierMessage: `Your identifier is ${identifier}`,
          attributeMessage: `Your value is ${Attribute1}`,
        },
      });
    } catch (error) {
      console.error('Error fetching data:', error);
      this.setState({
        response: {
          identifierMessage: '',
          attributeMessage: 'Error fetching data',
        },
      });
    }
  }

  render() {
    const { response } = this.state;

    return (
      <div>
        <form onSubmit={this.handleSubmit}>
          <label>Identifier:</label>
          <input
            type="text"
            name="name"
            onChange={this.handleChange}
            value={this.state.name}
          />

          <label>Value:</label>
          <input
            type="text"
            name="message"
            onChange={this.handleChange}
            value={this.state.message}
          />

          <button type="submit">Send</button>
        </form>
        <div>
          <h2>Response:</h2>
          <p>{response.identifierMessage}</p> {/* Display identifier message on one line */}
          <p>{response.attributeMessage}</p>  {/* Display attribute message on another line */}
        </div>
      </div>
    );
  }
}
