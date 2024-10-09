import React, { useState, useEffect } from 'react';
import './ToolOrLearn.css';
import './Selector.css';
import './WelcomeFlavor.css';
import './About.css';
import { useNavigate } from 'react-router-dom';
import AboutMe from './AboutMe';  // Import About component

const SplitAboutContact = () => {
    const [cursorX, setCursorX] = useState(window.innerWidth / 2);
    const navigate = useNavigate();

    useEffect(() => {
        const handleMouseMove = (e) => {
            const mouseX = e.clientX;
            const windowWidth = window.innerWidth;

            // Define the boundaries for the outer 25% on each side
            const leftBoundary = windowWidth * 0.35;
            const rightBoundary = windowWidth * 0.65;

            if (mouseX < leftBoundary) {
                // Invert cursor when in the left 25%
                const invertedCursorX = windowWidth - mouseX;
                setCursorX(invertedCursorX);
            } else if (mouseX > rightBoundary) {
                // Invert cursor when in the right 25%
                const invertedCursorX = windowWidth - mouseX;
                setCursorX(invertedCursorX);
            } else {
                // Set divider to center when in middle 50%
                setCursorX(windowWidth / 2);
            }
        };

        window.addEventListener('mousemove', handleMouseMove);
        return () => {
            window.removeEventListener('mousemove', handleMouseMove);
        };
    }, []);

    return (
        <div className="split-screen">
            <div className="content project-content" style={{ clipPath: `inset(0 ${window.innerWidth - cursorX}px 0 0)` }}>
                <h1>Portfolio</h1>
                <button
                    className="continue-button project-button"
                    onClick={() => navigate('/welcome-flavor')}
                >
                    Flavor Buddy
                </button>
            </div>

            <div className="content info-content" style={{ clipPath: `inset(0 0 0 ${cursorX}px)` }}>
            <div className='name-placement'>
            <h1>Robert Siewert</h1>
            </div>
                <button
                    className="continue-button info-button"
                    onClick={() => navigate('/about')}
                >
                    Info
                </button>
                <AboutMe />
            </div>
            <div className="divider" style={{ left: `${cursorX}px` }} />
        </div>
    );
};

export default SplitAboutContact;
