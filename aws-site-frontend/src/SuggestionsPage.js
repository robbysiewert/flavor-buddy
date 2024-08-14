import React from 'react';
import { useLocation } from 'react-router-dom';
import './SuggestionsPage.css'; // Import your custom CSS

const SuggestionsPage = () => {
    const { state } = useLocation();
    const { suggestions } = state || {};

    // Sort suggestions by rank
    const sortedSuggestions = Object.entries(suggestions || {}).sort(
        ([rankA], [rankB]) => parseInt(rankA) - parseInt(rankB)
    );

    return (
        <div className="suggestions-container">
            <h1>Suggested dishes based on your choices:</h1>
            <ul className="suggestions-list">
                {sortedSuggestions.map(([_, food], index) => (
                    <li
                        key={index}
                        className={`suggestion-item ${index === 0 ? 'top-suggestion' : ''}`}
                    >
                        {food}
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default SuggestionsPage;
