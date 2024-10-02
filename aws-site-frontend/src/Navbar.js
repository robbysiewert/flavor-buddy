import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import './Navbar.css';

const Navbar = () => {
    const [scrollingDown, setScrollingDown] = useState(false);
    let lastScrollY = 0;

    const handleScroll = () => {
        if (window.scrollY > lastScrollY) {
            setScrollingDown(true);
        } else {
            setScrollingDown(false);
        }
        lastScrollY = window.scrollY;
    };

    useEffect(() => {
        window.addEventListener('scroll', handleScroll);
        return () => {
            window.removeEventListener('scroll', handleScroll);
        };
    }, []);

    return (
        <nav className={`navbar ${scrollingDown ? 'hide' : ''}`}>
            <ul className="navbar-list">
                <li><Link to="/" className="navbar-link">Home</Link></li>
                <li><Link to="/about" className="navbar-link">About</Link></li>
                <li><Link to="/contact" className="navbar-link">Contact</Link></li>
            </ul>
        </nav>
    );
};

export default Navbar;
