import React from 'react';
import './About.css';
import './ToolOrLearn.css';
import { Link } from 'react-router-dom';


const AboutMe = () => {
    return (
        <div className="info">
        <div className='about-header-placement'>
        <h1>About</h1>
        </div>
        <div className='aboutme-content'>
        <p>Robert Siewert is a San Diego based Software Engineer with 2 years of experience building both on-premise and cloud-based solutions. His work spans from backend development using Java and Python to creating responsive front-end interfaces with Angular and React. Collaboration is at the heart of everything he does, and he excels at working cross-functionally with both technical teams and non-technical stakeholders to deliver impactful software.</p>
        <p>In his most recent role, he led the development of a full stack solution that integrated multiple REST APIs, leveraging AWS services like EC2, Lambda, S3, DynamoDB, and Cognito. This project secured a partnership with AWS. Before that, he automated operational workflows using Bash, Python, PHP, and MySQL, reducing manual work by 30% and maintaining high-quality software through new QA procedures.</p>
        <p>During his time at the University of California, Santa Barbara, he led a multi-disciplinary team of nine engineers to victory at the Navy’s Robot Rodeo Competition. Robert divided up tasks according to each team member’s strengths and built the software and automation for the robot himself. To the right, you can see Robert presenting the solution.</p>
        <p>Robert built user analytics and product recommendation features for a founder in his network at <a href="https://www.allkind.inc/">Allkind</a>. These features resulted in an 11% sales increase in the first month. This inspired his own personal recommendation project, <Link to="/welcome-flavor">Flavor Buddy</Link>.</p>
        <p></p>
        <p><a href="mailto:robbysiewert72@gmail.com">robbysiewert72@gmail.com</a></p>
        <p><a href="https://www.linkedin.com/in/robertsiewert">LinkedIn</a></p>
        <p><a href="https://github.com/robbysiewert">Github</a></p>
        </div>
        </div>
    );
};

export default AboutMe;
