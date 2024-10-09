import React from 'react';
import './About.css';
import './ToolOrLearn.css';
import auditoriumImage from './assets/auditorium.jpg';
import presentingImage from './assets/presenting.jpg';
import demoImage from './assets/demo.png';

const Images = () => {
    return (
        <div className="right-side">
            <img src={presentingImage} alt="Robot 1" />
            <img src={auditoriumImage} alt="Auditorium" />
            <img src={demoImage} alt="Presenting the Robot" />
        </div>
    );
};

export default Images;
