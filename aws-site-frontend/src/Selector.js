import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

const apiUrl = process.env.REACT_APP_API_GATEWAY_URL;

const Selector = () => {
    const [buttonNames, setButtonNames] = useState([]);
    const [selectedItems, setSelectedItems] = useState([]);
    const navigate = useNavigate();

    useEffect(() => {
        fetchButtonNames();
    }, []);

    const fetchButtonNames = async () => {
        try {
            const response = await axios.get(`${apiUrl}storage`, {
                params: {
                    requested_item: 'random_food'
                }
            });

            const { random_item1, random_item2, random_item3 } = response.data;
            setButtonNames([random_item1, random_item2, random_item3]);
        } catch (error) {
            console.error('Error fetching button names:', error);
        }
    };

    const handleButtonClick = async (buttonName) => {
        try {
            await axios.post(`${apiUrl}storage`, { id: buttonName });
            setSelectedItems([...selectedItems, buttonName]);
            fetchButtonNames();
        } catch (error) {
            console.error('Error making POST request:', error);
        }
    };

    const handleFinishClick = async () => {
        try {
            const response = await axios.get(`${apiUrl}storage`, {
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
        <div>
            <h1>What are you in the mood for today?</h1>
            {buttonNames.length > 0 ? (
                buttonNames.map((name, index) => (
                    <button key={index} onClick={() => handleButtonClick(name)}>
                        {name}
                    </button>
                ))
            ) : (
                <p>Loading options...</p>
            )}
            {selectedItems.length >= 3 && (
                <button onClick={handleFinishClick}>Finish</button>
            )}
        </div>
    );
};

export default Selector;
