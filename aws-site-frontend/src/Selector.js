import React, { useState } from 'react';
import axios from 'axios';

const apiUrl = process.env.REACT_APP_API_GATEWAY_URL;

const ItemSelector = () => {
    const [relatedItems, setRelatedItems] = useState([]);

    const handleSelection = (category) => {
        // Call the Lambda function via API Gateway
        axios.post(`${apiUrl}storage`, { category })
            .then(response => {
                setRelatedItems(response.data.body);
            })
            .catch(error => {
                console.error('Error fetching related items:', error);
            });
    };

    return (
        <div>
            <h3>Select an item:</h3>
            <button onClick={() => handleSelection('cupcake')}>Cupcake</button>
            <button onClick={() => handleSelection('candy')}>Candy</button>
            <button onClick={() => handleSelection('brownie')}>Brownie</button>

            {relatedItems.length > 0 && (
                <div>
                    <h4>Related Items:</h4>
                    <ul>
                        {relatedItems.map(item => (
                            <li key={item.itemId}>{item.name}</li>
                        ))}
                    </ul>
                </div>
            )}
        </div>
    );
};

export default ItemSelector;
