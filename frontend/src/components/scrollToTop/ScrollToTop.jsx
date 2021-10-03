import React, { useState, useEffect, useCallback } from 'react';
import styles from './ScrollToTop.module.css';
import cx from 'classnames';

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
            //if (scrollY > window.scrollY && (scrollY !== 0 && window.scrollY !== 0)) {
            if (scrolled > 4340 && scrollY > window.scrollY && (scrollY !== 0 && window.scrollY !== 0)) {
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

    const scrollClasses =  cx({
        'scroll-to-top-visible': isVisible && isMobile,
        'scroll-to-top-not-visible': !(isVisible && isMobile)
    });

    return (
        <div>
            <button onClick={scroll}
            className={cx(styles['scroll-to-top-button'], styles[scrollClasses])} >
                Back to top <i className="fas fa-angle-double-up 2x"></i>
            </button>
        </div>
    );
}

export default ScrollToTop;
