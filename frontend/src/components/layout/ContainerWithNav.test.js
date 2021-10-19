import React from 'react';
import { render, fireEvent } from '@testing-library/react';
import ContainerWithNav from './ContainerWithNav';

const mockHistoryPush = jest.fn();
const mockHandleRemoveAuth = jest.fn();
const mockLogout = jest.fn();

jest.mock('react-router-dom', () => ({
    ...jest.requireActual('react-router-dom'),
    useHistory: () => ({
      push: mockHistoryPush
    })
}));

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
            handleRemoveAuth: mockHandleRemoveAuth
        })
    };
});

jest.mock('../../WwcApi', () => {
    return {
        logout: jest.fn(() => mockLogout)
    };
});

describe('ContainerWithNav', () => {
    afterEach(() => {
        mockHistoryPush.mockClear();
    });

    test('it renders without crashing', () => {
        const { container } = render(<ContainerWithNav />);
        expect(container).toMatchSnapshot();
    });

    test('it goes to profile on profile button click', () => {
        const { container, getByText } = render(<ContainerWithNav />);
        const profileButton = getByText(/Your Profile/i);

        fireEvent.click(profileButton);
        expect(mockHistoryPush).toBeCalledWith({ pathname: '/member/profile' });
    });

    test('it logs out on logout button click', () => {
        const { container, getByText } = render(<ContainerWithNav />);
        const logoutButton = getByText(/Log Out/i);

        fireEvent.click(logoutButton);
        
        setTimeout(() => {
            expect(mockLogout).toHaveBeenCalledTimes(1);
            expect(mockHandleRemoveAuth).toHaveBeenCalledTimes(1);
            expect(mockHistoryPush).toBeCalledWith({ pathname: '/login' });
        }, 100);
    });
});