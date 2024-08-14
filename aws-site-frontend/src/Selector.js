import React, { useEffect, useState } from 'react';
import axios from 'axios';

const apiUrl = process.env.REACT_APP_API_GATEWAY_URL;

const ButtonsPage = () => {
    const [buttonNames, setButtonNames] = useState([]);

    const fetchButtonNames = async () => {
        try {
            // Make a single GET request with queryStringParameters
            const response = await axios.get(`${apiUrl}storage`, {
                params: {
                    requested_item: 'random_food'
                }
            });

            // Extract the food names from the response
            const { random_item1, random_item2, random_item3 } = response.data;

            // Set the button names in state
            setButtonNames([random_item1, random_item2, random_item3]);
        } catch (error) {
            console.error('Error fetching button names:', error);
        }
    };

    useEffect(() => {
        fetchButtonNames(); // Fetch button names when the component mounts
    }, []);

    // Handler for button click
    const handleButtonClick = async (buttonName) => {
        try {
            await axios.post(`${apiUrl}storage`, { id: buttonName });
            console.log(`POST request successful for button: ${buttonName}`);
            fetchButtonNames(); // Refresh button names after a button is clicked
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
