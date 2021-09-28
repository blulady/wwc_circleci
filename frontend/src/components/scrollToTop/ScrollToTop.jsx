import React, { useState, useEffect } from 'react';
import { FaArrowCircleUp } from 'react-icons/fa';
import styles from './ScrollToTop.module.css';

const ScrollToTop = () => {
    const [isVisible, setIsVisible] = useState(false);
    const [isMobile, setIsMobile] = useState(false);

    useEffect(() => {
        checkIsMobile();
    }, []);

    const toggleButton = () => {
        const scrolled = document.documentElement.scrollTop;

        if (scrolled > 200) {
            setIsVisible(true);
        } else {
            setIsVisible(false);
        }
    };

    const scroll = () => {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    };

    const checkIsMobile = () => {
        const resolution = window.innerWidth;

        if (resolution <= 480) {
            setIsMobile(true);
        }
    };

    window.addEventListener('scroll', toggleButton);

    return (
        <React.Fragment>
            <FaArrowCircleUp onClick={scroll}
            style={{display : isVisible && isMobile ? 'inline' : 'none'}}
            className={styles['scroll-to-top-button']} />
        </React.Fragment>
    );
}

export default ScrollToTop;
