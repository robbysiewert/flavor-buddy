import React, { useState, useEffect } from 'react';
import './ToolOrLearn.css';
import './Selector.css';
import './WelcomeFlavor.css';
import './About.css';
import { useNavigate } from 'react-router-dom';

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
            <div className="info">
            <h2>About</h2>
            <p>Robert Siewert is a San Diego based Software Engineer with 2 years of experience building both on-premise and cloud-based solutions. His work spans from backend development using Java and Python to creating responsive front-end interfaces with Angular and React. Collaboration is at the heart of everything he does, and excels at working cross-functionally with both technical teams and non-technical stakeholders to deliver impactful software.</p>
            <p>In his most recent role, he led the development of a full stack solution that integrated multiple REST APIs, leveraging AWS services like EC2, Lambda, S3, DynamoDB, and Cognito. This project secured a partnership with AWS. Before that, he automated operational workflows using Bash, Python, PHP, and MySQL, reducing manual work by 30% and maintaining high-quality software through new QA procedures.</p>
            <p>Robert built user analytics and product recommendation features for a founder in his network at Allkind <a href="https://www.allkind.inc/">Allkind</a>. These features resulted in an 11% sales increase in the first month. This inspired his own personal recommendation project, Flavor Buddy <a href="/welcome-flavor">Flavor Buddy</a>.</p>
            <p>During his time at the University of California, Santa Barbara, he led a multi-disciplinary team of nine engineers to victory at the Navy’s Robot Rodeo Competition. Robert divided up tasks according to each team member’s strengths and built the software and automation for the robot himself. To the right, you can see Robert presenting the solution.</p>
            </div>
                <h1>Robert Siewert</h1>
                <button
                    className="continue-button info-button"
                    onClick={() => navigate('/about')}
                >
                    Info
                </button>
            </div>
            <div className="divider" style={{ left: `${cursorX}px` }} />
        </div>
    );
};

export default SplitAboutContact;
