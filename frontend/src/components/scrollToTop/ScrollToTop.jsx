import React, { useState } from 'react';
import { FaArrowCircleUp } from 'react-icons/fa';
import styles from './ScrollToTop.module.css';

const ScrollToTop = () => {
    const [visible, setVisible] = useState(false);

    const toggleButton = () => {
        const scrolled = document.documentElement.scrollTop;
        if (scrolled > 200) {
            setVisible(true);
        } else {
            setVisible(false);
        }
    };

    const scroll = () => {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    };

    window.addEventListener('scroll', toggleButton);

    return (
        <React.Fragment>
            <FaArrowCircleUp onClick={scroll}
            style={{display : visible ? 'inline' : 'none'}}
            className={styles['scroll-to-top-button']} />
        </React.Fragment>
    );
}

export default ScrollToTop;
