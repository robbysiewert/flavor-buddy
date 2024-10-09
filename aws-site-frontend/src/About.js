import React from 'react';
import './About.css';
import './ToolOrLearn.css';
import Images from './Images';
import AboutMe from './AboutMe';

const About = () => {
    return (
        <div className="about-content info-content">
        <AboutMe />
        <Images />
        </div>
    );
};

export default About;
