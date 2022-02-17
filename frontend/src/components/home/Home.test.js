import React from 'react';
import { render } from '@testing-library/react';
import Home from './Home';

jest.mock('react-router-dom', () => ({
    useHistory: () => ({
      push: jest.fn()
    })
}));

jest.mock('react', () => {
    const ActualReact = jest.requireActual('react');
    return {
        ...ActualReact,
        useContext: () => ({
            userInfo: {
                email: 'director@example.com',
                first_name: 'John',
                id: 1,
                last_name: 'Smith',
                role: 'DIRECTOR'
            },
            handleRemoveAuth: jest.fn()
        })
    };
});

describe('Home', () => {
    test('it renders without crashing', () => {
        const { container } = render(<Home />);
        expect(container).toMatchSnapshot();
    });
});