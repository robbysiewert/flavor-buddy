import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import './Selector.css';

const apiUrl = process.env.REACT_APP_API_GATEWAY_URL;

const Selector = () => {
    const [buttonNames, setButtonNames] = useState([]);
    const [selectedItems, setSelectedItems] = useState([]);
    const [remainingSets, setRemainingSets] = useState(3); // Initialize remaining sets
    const [buttonKey, setButtonKey] = useState(0); // Key to reset buttons
    const navigate = useNavigate();

    useEffect(() => {
        fetchButtonNames();
    }, []);

    const fetchButtonNames = async () => {
        try {
            console.log('Fetching button names');
            console.log('API URL:', apiUrl);
            const response = await axios.get(`${apiUrl}`, {
                params: {
                    requested_item: 'random_food'
                }
            });
            console.log('Response data:', response.data);
            const { random_item1, random_item2, random_item3 } = response.data;
            setButtonNames([random_item1, random_item2, random_item3]);
            setButtonKey(prevKey => prevKey + 1); // Update key to trigger animation
        } catch (error) {
            console.error('Error fetching button names:', error);
        }
    };

    const handleButtonClick = async (buttonName) => {
        try {
            await axios.post(`${apiUrl}`, { id: buttonName });
            setSelectedItems([...selectedItems, buttonName]);

            // Decrement remaining sets but ensure it doesn't go below 0
            setRemainingSets(prev => (prev > 0 ? prev - 1 : 0));

            fetchButtonNames();
        } catch (error) {
            console.error('Error making POST request:', error);
        }
    };

    const handleFinishClick = async () => {
        try {
            const response = await axios.get(`${apiUrl}`, {
                params: {
                    requested_item: 'food_suggestions'
                }
            });

            const suggestions = response.data;
            navigate('/suggestions', { state: { suggestions } });
        } catch (error) {
            console.error('Error fetching suggestions:', error);
        }
    };

    return (
        <div className="selector-container">
            <div className="instructions">
                <h1>Pick your favorites</h1>
                <p>
                    {remainingSets > 0
                        ? `Select an option from at least ${remainingSets} more ${remainingSets === 1 ? 'set' : 'sets'}`
                        : "Select another option for better results"}
                </p>
            </div>
            <div className="buttons-container">
            {buttonNames.length > 0 ? (
                buttonNames.map((name, index) => (
                    <div key={`${buttonKey}-${index}`} className="button-wrapper">
                        <button onClick={() => handleButtonClick(name)}>
                            {name}
                        </button>
                    </div>
                ))
            ) : (
                <p>Retrieving options...</p>
            )}
        </div>
            <div className="actions-container">
                <button onClick={fetchButtonNames}>
                    Skip
                </button>
                {selectedItems.length >= 3 && (
                    <button onClick={handleFinishClick}>
                        Finish
                    </button>
                )}
            </div>
        </div>
    );
};

export default Selector;
