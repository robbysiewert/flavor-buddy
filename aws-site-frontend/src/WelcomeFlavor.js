// WelcomePage.js
import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import './WelcomeFlavor.css';

const apiUrl = process.env.REACT_APP_API_GATEWAY_URL;

const WelcomePage = () => {
    const navigate = useNavigate();

    useEffect(() => {
        const postUserData = async () => {
            try {
                await axios.post(`${apiUrl}`, { id: 'add_user_data' });
                console.log('User reset successful');
            } catch (error) {
                console.error('Error making initial POST request:', error);
            }
        };

        postUserData();
    }, []);

    const handleContinue = () => {
        navigate('/selector');
    };

    return (
            <div className="welcome-container">
                <h1>Hi, I'm Flavor Buddy</h1>
                <p>Select your favorite foods, and I'll suggest the top choices for you to try</p>
                <button onClick={handleContinue} className="continue-button">
                    Continue
                </button>
            </div>
    );
};

export default WelcomePage;
