import React from 'react';
import { Router } from 'react-router-dom';
import { render } from '@testing-library/react';
import { createMemoryHistory } from 'history';
import PrivateRoute from './PrivateRoute';
import Home from './components/home/Home';

let mockToken = {
    access: 'ABCD',
    refresh: 'EFGH'
}
const mockHandleRemoveAuth = jest.fn();
const mockHistory = createMemoryHistory('/home');

jest.mock('react', () => {
    const ActualReact = require.requireActual('react');
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
            handleRemoveAuth: mockHandleRemoveAuth,
            token: mockToken
        })
    };
});

describe('PrivateRoute', () => {
    test('it renders without crashing', () => {
        const { container } = render(<Router history={mockHistory}>
                                        <PrivateRoute exact path='/home' />
                                            <Home />
                                    </Router>);
        
        expect(container).toMatchSnapshot();
    });

    test('it shows the route with valid token', () => {
        const { getByText } = render(<Router history={mockHistory}>
                                        <PrivateRoute exact path='/home' />
                                            <Home />
                                    </Router>);
        const membersTitle = getByText(/Chapter Members/i);

        expect(membersTitle).toBeInTheDocument();
    });

    test('it redirects to login with no token', () => {
        mockToken = null;
        const { getByText } = render(<Router history={mockHistory}>
                                        <PrivateRoute exact path='/home' />
                                            <Home />
                                    </Router>);

        expect(mockHistory.location.pathname).toBe('/login');
    });
});