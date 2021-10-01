import React, { useState, useEffect, useCallback } from 'react';
import styles from './ScrollToTop.module.css';

const ScrollToTop = () => {
    const [isVisible, setIsVisible] = useState(false);
    const [isMobile, setIsMobile] = useState(false);
    const [scrollY, setScrollY] = useState(window.scrollY);

    const checkIsMobile = () => {
        const resolution = window.innerWidth;

        if (resolution <= 480) {
            setIsMobile(true);
        }
    };

    const handleScroll = useCallback(
        (e) => {
            const scrolled = document.documentElement.scrollTop;
            const window = e.currentTarget;

            // Comment out if statement and use comment below to see button 
            //if (scrollY > window.scrollY) {
            if (scrolled > 4340 && scrollY > window.scrollY) {
                setIsVisible(true);
            } else {
                setIsVisible(false);
            }

            setScrollY(window.scrollY);
        },
        [scrollY],
    );

    const scroll = () => {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });

        setIsVisible(false);
    };

    useEffect(() => {
        checkIsMobile();
    }, []);

    useEffect(() => {
        setScrollY(window.scrollY);

        window.addEventListener("scroll", handleScroll);

        return () => {
            window.removeEventListener("scroll", handleScroll);
        }
    }, [handleScroll]);

    return (
        <div>
            <button onClick={scroll}
            style={{display : isVisible && isMobile ? 'inline' : 'none'}}
            className={styles['scroll-to-top-button']} >
                Back to top <i className="fas fa-angle-double-up 2x"></i>
            </button>
        </div>
    );
}

export default ScrollToTop;
