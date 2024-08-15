import React from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import './SuggestionsPage.css'; // Import your custom CSS

const SuggestionsPage = () => {
    const { state } = useLocation();
    const { suggestions } = state || {};
    const navigate = useNavigate();

    // Sort suggestions by rank
    const sortedSuggestions = Object.entries(suggestions || {}).sort(
        ([rankA], [rankB]) => parseInt(rankA) - parseInt(rankB)
    );

    const handleTryAgain = () => {
        navigate('/selector');
    };

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
            <button onClick={handleTryAgain} className="try-again-button">
                Try Again
            </button>
        </div>
    );
};

export default SuggestionsPage;
