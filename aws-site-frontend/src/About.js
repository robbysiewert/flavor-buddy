import React from 'react';
import './About.css';
import './ToolOrLearn.css';
import Images from './Images';
import AboutMe from './AboutMe';

const About = () => {
    return (
        <div className="about-content">
        <div className="content info-content">
        <AboutMe />
        </div>
        <Images />
        </div>
    );
};

export default About;
