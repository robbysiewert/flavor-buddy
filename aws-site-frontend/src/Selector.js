import React, { useEffect, useState } from 'react';
import axios from 'axios';

const apiUrl = process.env.REACT_APP_API_GATEWAY_URL;

const ButtonsPage = () => {
    const [buttonNames, setButtonNames] = useState([]);

    useEffect(() => {
        const fetchButtonNames = async () => {
            try {
                // Create an array of promises for calling the Lambda function three times
                const promises = [
                    axios.get(`${apiUrl}storage`),
                    axios.get(`${apiUrl}storage`),
                    axios.get(`${apiUrl}storage`)
                ];

                // Wait for all promises to resolve
                const responses = await Promise.all(promises);

                // Extract messages from responses
                const names = responses.map(response => response.data.message);

                // Set the button names in state
                setButtonNames(names);
            } catch (error) {
                console.error('Error fetching button names:', error);
            }
        };

        fetchButtonNames();
    }, []);

    // Handler for button click
    const handleButtonClick = async (buttonName) => {
        try {
            await axios.post(`${apiUrl}storage`, { id: buttonName });
            console.log(`POST request successful for button: ${buttonName}`);
        } catch (error) {
            console.error('Error making POST request:', error);
        }
    };

    return (
        <div>
            {buttonNames.map((name, index) => (
                <button key={index} onClick={() => handleButtonClick(name)}>
                    {name}
                </button>
            ))}
        </div>
    );
};

export default ButtonsPage;
