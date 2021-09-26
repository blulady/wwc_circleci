import React, { useState } from 'react';
import { FaArrowCircleUp } from 'react-icons/fa';

const ScrollToTop = () => {
    const [visible, setVisible] = useState(false);

    const toggleButton = () => {
        const scrolled = document.documentElement.scrollTop;
        if (scrolled > 100) {
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
            style={{display : visible ? 'inline' : 'none'}} />
        </React.Fragment>
    );
}

export default ScrollToTop;
