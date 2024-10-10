import React, { useState, useEffect, useCallback, useRef } from 'react';
import { Link } from 'react-router-dom';
import './Navbar.css';

const Navbar = () => {
    const [scrollingDown, setScrollingDown] = useState(false);
    const lastScrollY = useRef(0); // Use useRef to persist the value across renders

    const handleScroll = useCallback(() => {
        if (window.scrollY > lastScrollY.current) {
            setScrollingDown(true);
        } else {
            setScrollingDown(false);
        }
        lastScrollY.current = window.scrollY; // Update the value using the ref
    }, []);  // The empty array ensures this is only created once

    useEffect(() => {
        window.addEventListener('scroll', handleScroll);
        return () => {
            window.removeEventListener('scroll', handleScroll);
        };
    }, [handleScroll]);  // Add handleScroll as a dependency

    return (
        <nav className={`navbar ${scrollingDown ? 'hide' : ''}`}>
            <ul className="navbar-list">
                <li><Link to="/" className="navbar-link">Home</Link></li>
                <li><Link to="/about" className="navbar-link">About</Link></li>
            </ul>
        </nav>
    );
};

export default Navbar;
