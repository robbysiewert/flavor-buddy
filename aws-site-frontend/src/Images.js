import React, { useEffect } from 'react';
import './About.css';
import './ToolOrLearn.css';
import auditoriumImage from './assets/auditorium.jpg';
import presentingImage from './assets/presenting.jpg';
import demoImage from './assets/demo.png';

const Images = () => {
    useEffect(() => {
        const images = document.querySelectorAll('.slide-in');
        images.forEach((image, index) => {
            setTimeout(() => {
                image.classList.add('in-view');
            }, index * 300); // Stagger the animation for each image
        });
    }, []);

    return (
        <div className="right-side">
            <img src={presentingImage} alt="Robert Presenting" className="slide-in" />
            <img src={auditoriumImage} alt="Auditorium" className="slide-in" />
            <img src={demoImage} alt="Robot Demo" className="slide-in" />
        </div>
    );
};

export default Images;
