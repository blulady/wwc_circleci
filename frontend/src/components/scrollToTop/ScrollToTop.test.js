import React from 'react';
import { render, fireEvent, act } from '@testing-library/react';
import ScrollToTop from './ScrollToTop';

describe('ScrollToTop', () => {
    test('it renders without crashing', () => {
        const { container } = render(<ScrollToTop />);
        expect(container).toMatchSnapshot();
    });

    test('it does not display button when scrollY > 4340 and user is scrolling up and not on mobile', () => {
        const { getByText } = render(<ScrollToTop />);
        fireEvent.scroll(global, { target: { scrollY: 4350 } });
        fireEvent.scroll(global, { target: { scrollY: 4341 } });
        const button = getByText(/Back to Top/i);

        expect(button).toHaveClass('scroll-to-top-not-visible');
    });

    test('it displays button when scrollY > 4340 and user is scrolling up and on mobile', () => {
        global.innerWidth = 414;
        global.dispatchEvent(new Event('resize'));

        const { container, getByText } = render(<ScrollToTop />);
        const scrollTopSpy = jest.spyOn(document.documentElement, 'scrollTop', 'get')
                                .mockImplementation(() => 4350);

        fireEvent.scroll(global, { target: { scrollY: 4350 } });
        fireEvent.scroll(global, { target: { scrollY: 4341 } });

        const button = getByText(/Back to Top/i);
        expect(button).toHaveClass('scroll-to-top-visible');
    });

    test('when button is pressed, it scrolls to top and does not display button', () => {
        global.innerWidth = 414;
        global.dispatchEvent(new Event('resize'));

        const { container, getByText } = render(<ScrollToTop />);
        const scrollTopSpy = jest.spyOn(document.documentElement, 'scrollTop', 'get')
                                 .mockImplementation(() => 4350);
        window.scrollTo = jest.fn();
        let button;

        act(() => {
            fireEvent.scroll(global, { target: { scrollY: 4350 } });
            fireEvent.scroll(global, { target: { scrollY: 4341 } });
            button = getByText(/Back to Top/i);
            fireEvent.click(button);
        });

        expect(window.scrollTo).toHaveBeenCalled();
        expect(button).toHaveClass('scroll-to-top-not-visible');
    });
});