import React from 'react';
import { useLocation } from 'react-router-dom';

const SuggestionsPage = () => {
    const location = useLocation();
    const suggestions = location.state?.suggestions || {};

    const topThreeSuggestions = Object.keys(suggestions)
        .slice(0, 3)
        .map((key) => suggestions[key]);

    return (
        <div>
            <h2>Suggestions:</h2>
            <ul>
                {topThreeSuggestions.map((suggestion, index) => (
                    <li key={index}>{suggestion}</li>
                ))}
            </ul>
        </div>
    );
};

export default SuggestionsPage;
