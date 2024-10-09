import React from 'react';
import './About.css';
import './ToolOrLearn.css';
import auditoriumImage from './assets/auditorium.jpg';
import presentingImage from './assets/presenting.jpg';
import demoImage from './assets/demo.png';

const About = () => {
    return (
        <div className="about-content">
        <div className="info">
        <h2>About</h2>
        <p>Robert Siewert is a San Diego based Software Engineer with 2 years of experience building both on-premise and cloud-based solutions. His work spans from backend development using Java and Python to creating responsive front-end interfaces with Angular and React. Collaboration is at the heart of everything he does, and excels at working cross-functionally with both technical teams and non-technical stakeholders to deliver impactful software.</p>
        <p>In his most recent role, he led the development of a full stack solution that integrated multiple REST APIs, leveraging AWS services like EC2, Lambda, S3, DynamoDB, and Cognito. This project secured a partnership with AWS. Before that, he automated operational workflows using Bash, Python, PHP, and MySQL, reducing manual work by 30% and maintaining high-quality software through new QA procedures.</p>
        <p>Robert built user analytics and product recommendation features for a founder in his network at Allkind <a href="https://www.allkind.inc/">Allkind</a>. These features resulted in an 11% sales increase in the first month. This inspired his own personal recommendation project, Flavor Buddy <a href="/welcome-flavor">Flavor Buddy</a>.</p>
        <p>During his time at the University of California, Santa Barbara, he led a multi-disciplinary team of nine engineers to victory at the Navy’s Robot Rodeo Competition. Robert divided up tasks according to each team member’s strengths and built the software and automation for the robot himself. To the right, you can see Robert presenting the solution.</p>
    </div>

        <div className="right-side">
        <img src={presentingImage} alt="Robot 1" />
        <img src={auditoriumImage} alt="Auditorium" />
        <img src={demoImage} alt="Presenting the Robot" />
    </div>
            </div>
    );
};

export default About;
