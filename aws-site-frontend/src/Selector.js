import React, { useEffect, useState } from 'react';
import axios from 'axios';

const apiUrl = process.env.REACT_APP_API_GATEWAY_URL;

const Selector = () => {
    const [buttonNames, setButtonNames] = useState([]);
    const [selectedFoods, setSelectedFoods] = useState([]);
    const [suggestions, setSuggestions] = useState(null);

    const fetchButtonNames = async () => {
        try {
            const response = await axios.get(`${apiUrl}storage`, {
                params: { requested_item: 'random_food' }
            });

            const { random_item1, random_item2, random_item3 } = response.data;
            setButtonNames([random_item1, random_item2, random_item3]);
        } catch (error) {
            console.error('Error fetching button names:', error);
        }
    };

    useEffect(() => {
        fetchButtonNames();
    }, []);

    const handleButtonClick = async (buttonName) => {
        try {
            await axios.post(`${apiUrl}storage`, { id: buttonName });
            setSelectedFoods(prevSelectedFoods => [...prevSelectedFoods, buttonName]);
            fetchButtonNames();
        } catch (error) {
            console.error('Error making POST request:', error);
        }
    };

    const handleFinishClick = async () => {
        try {
            const response = await axios.get(`${apiUrl}storage`, {
                params: { requested_item: 'food_suggestions' }
            });
            console.log(`GET request successful: food_suggestions`);

            const { suggestions } = response.data;
            setSuggestions(suggestions);
        } catch (error) {
            console.error('Error fetching suggestions:', error);
        }
    };

    if (suggestions) {
        return (
            <div>
                <h2>Suggestions:</h2>
                <ul>
                    {suggestions.map((suggestion, index) => (
                        <li key={index}>{suggestion}</li>
                    ))}
                </ul>
            </div>
        );
    }

    return (
        <div>
            {buttonNames.map((name, index) => (
                <button key={index} onClick={() => handleButtonClick(name)}>
                    {name}
                </button>
            ))}
            {selectedFoods.length >= 3 && (
                <button onClick={handleFinishClick}>Finish</button>
            )}
        </div>
    );
};

export default Selector;