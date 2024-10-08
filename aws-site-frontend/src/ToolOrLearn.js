import React, { useState, useEffect } from 'react';
import './ToolOrLearn.css';

const SplitAboutContact = () => {
    const [cursorX, setCursorX] = useState(window.innerWidth / 2);

    useEffect(() => {
        const handleMouseMove = (e) => {
            const invertedCursorX = window.innerWidth - e.clientX; // Invert cursor movement
            setCursorX(invertedCursorX);  // Move the divider in the opposite direction
        };

        window.addEventListener('mousemove', handleMouseMove);
        return () => {
            window.removeEventListener('mousemove', handleMouseMove);
        };
    }, []);

    return (
        <div className="split-screen">
            <div className="content left-content" style={{ clipPath: `inset(0 0 0 ${cursorX}px)` }}>
                <h1>Robert Siewert</h1>
                <p>Software Engineer</p>
                <button className="left-button">Robert Siewert</button>
            </div>
            <div className="content right-content" style={{ clipPath: `inset(0 ${window.innerWidth - cursorX}px 0 0)` }}>
                <h1>Flavor Buddy</h1>
                <p>Get meal suggestions to spice things up</p>
                <button className="right-button">Flavor Buddy</button>
            </div>
            <div className="divider" style={{ left: `${cursorX}px` }} />
        </div>
    );
};

export default SplitAboutContact;
