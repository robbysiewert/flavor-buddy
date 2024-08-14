// WelcomePage.js
import React from 'react';
import { useNavigate } from 'react-router-dom';
import './WelcomePage.css'; // Import your custom CSS

const WelcomePage = () => {
    const navigate = useNavigate();

    const handleContinue = () => {
        navigate('/selector'); // Replace '/selector' with the route to your main content page
    };

    return (
        <div className="welcome-container">
            <h1>Welcome to Flavor Buddy!</h1>
            <p>
                I'll help you find the best food options based on your preferences.
                You can select your favorite foods, and I'll suggest the top choices for you to try.
            </p>
            <button onClick={handleContinue} className="continue-button">
                Continue
            </button>
        </div>
    );
};

export default WelcomePage;
