import React from 'react';
import { Route, Router, Routes } from 'react-router-dom';
import { render } from '@testing-library/react';
import { createMemoryHistory } from 'history';
import PrivateRoute from './PrivateRoute';
import Home from './components/home/Home';
import * as TeamContext from './context/team/TeamContext';
import * as AuthContext from './context/auth/AuthContext';
import { act } from 'react-dom/test-utils';
import WwcApi from './WwcApi';

const mockToken = {
    access: 'ABCD',
    refresh: 'EFGH'
}
const mockHandleRemoveAuth = jest.fn();
const mockHistory = createMemoryHistory({initialEntries: ['/home']})

const contextTeams = { teams: [{ id: 5, name: 'Team1' }] };
const contextAuth = {
    userInfo: {
        email: 'director@example.com',
        first_name: 'John',
        id: 1,
        last_name: 'Smith',
        role: 'DIRECTOR'
    },
    handleRemoveAuth: mockHandleRemoveAuth,
    token: mockToken
};

describe('PrivateRoute', () => {
    const setupMocks = (token) => {
        jest.spyOn(AuthContext, 'useAuthContext').mockImplementation(() => {
            return { ...contextAuth, token: token };
        });
        jest.spyOn(WwcApi, 'getTeams').mockImplementation(async () => {
            return Promise.resolve(contextTeams.teams);
        });
    };

    afterEach(() => {
        jest.resetAllMocks();
    });

    test('it renders without crashing', async () => {
        setupMocks(mockToken);
        let res;
        await act(async () => {
            res = render(
                <Router navigator={mockHistory} location={mockHistory.location}>
                    <Routes>
                        <Route path="/home" element={<PrivateRoute element={<Home />} />} />
                    </Routes>
                </Router>
            );
        })

        expect(res.container).toMatchSnapshot();
    });

    test('it shows the route with valid token', async () => {
        setupMocks(mockToken);
        let res;
        await act(async () => {
            res = render(
                <Router navigator={mockHistory} location={mockHistory.location}>
                    <Routes>
                        <Route path="/home" element={<PrivateRoute element={<Home />} />} />
                    </Routes>
                </Router>
            );
        })

        const membersTitle = res.getByText(/Chapter Members/i);
        expect(membersTitle).toBeInTheDocument();
    });

    test('it redirects to login with no token', () => {
        setupMocks(null);
        render(
            <Router navigator={mockHistory} location={mockHistory.location}>
                <Routes>
                    <Route path="/home" element={<PrivateRoute element={<Home />} />} />
                </Routes>
            </Router>
        );

        expect(mockHistory.location.pathname).toBe('/login');
    });
});