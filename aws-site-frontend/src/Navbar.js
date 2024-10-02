// Navbar.js
import React from 'react';
import { Link } from 'react-router-dom';
import './Navbar.css'; // Import the Navbar CSS

const Navbar = () => {
    return (
        <nav className="navbar">
            <ul className="navbar-list">
                <li><Link to="/" className="navbar-link">Home</Link></li>
                <li><Link to="/about" className="navbar-link">About</Link></li>
                <li><Link to="/contact" className="navbar-link">Contact</Link></li>
            </ul>
        </nav>
    );
};

export default Navbar;
