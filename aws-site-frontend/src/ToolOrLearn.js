import React, { useState, useEffect, useRef } from 'react';
import './ToolOrLearn.css';
import './WelcomeFlavor.css';
import { useNavigate } from 'react-router-dom';
import AboutMe from './AboutMe';

const SplitAboutContact = () => {
    const [cursorX, setCursorX] = useState(window.innerWidth / 2);
    const navigate = useNavigate();
    const projectRef = useRef(null);
    const infoRef = useRef(null);

    useEffect(() => {
        // Match the height of project-content to info-content
        const projectContent = projectRef.current;
        const infoContent = infoRef.current;

        if (projectContent && infoContent) {
            const infoContentHeight = infoContent.offsetHeight;
            projectContent.style.height = `${infoContentHeight}px`;
        }
    }, []); // This effect runs once on mount

    useEffect(() => {
        const handleMouseMove = (e) => {
            const mouseX = e.clientX;
            const windowWidth = window.innerWidth;

            const leftBoundary = windowWidth * 0.35;
            const rightBoundary = windowWidth * 0.65;
            const center = windowWidth * 0.50;
            const invertedCursorX = windowWidth - mouseX;

            if (mouseX < leftBoundary || mouseX > rightBoundary) {
                setCursorX(invertedCursorX);
            } else {
                setCursorX(center);
            }
        };

        window.addEventListener('mousemove', handleMouseMove);
        return () => {
            window.removeEventListener('mousemove', handleMouseMove);
        };
    }, []);

    return (
        <div className="split-screen">
            <div
                ref={projectRef}
                className="content project-content"
                style={{ clipPath: `inset(0 ${window.innerWidth - cursorX}px 0 0)` }}
            >
                <h1>Portfolio</h1>
                <button
                    className="continue-button project-button"
                    onClick={() => navigate('/welcome-flavor')}
                >
                    Flavor Buddy
                </button>
                <p>Flavor buddy is a user analytics / product recommendation tool. Find out what meal to order tonight.</p>
            </div>

            <div
                ref={infoRef}
                className="content info-content"
                style={{ clipPath: `inset(0 0 0 ${cursorX}px)` }}
            >
                <h1>Robert Siewert</h1>
                <button
                    className="continue-button info-button"
                    onClick={() => navigate('/about')}
                >
                    About
                </button>
                <AboutMe />
            </div>
            <div className="divider" style={{ left: `${cursorX}px` }} />
        </div>
    );
};

export default SplitAboutContact;
