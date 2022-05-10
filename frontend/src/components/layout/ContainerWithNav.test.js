import React from 'react';
import { render, fireEvent } from '@testing-library/react';
import ContainerWithNav from './ContainerWithNav';
import WwcApi from '../../WwcApi';

const mockNavigation = jest.fn();
const mockHandleRemoveAuth = jest.fn();

jest.mock('react-router-dom', () => ({
    ...jest.requireActual('react-router-dom'),
    useNavigate: () => mockNavigation
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
            handleRemoveAuth: mockHandleRemoveAuth
        })
    };
});

describe('ContainerWithNav', () => {
    afterEach(() => {
        mockNavigation.mockClear();
    });

    test('it renders without crashing', () => {
        const { container } = render(<ContainerWithNav />);

        expect(container).toMatchSnapshot();
    });

    test('it goes to profile on profile button click', () => {
        const { getByText } = render(<ContainerWithNav />);
        const profileButton = getByText(/Your Profile/i);

        fireEvent.click(profileButton);

        expect(mockNavigation).toBeCalledWith('/member/profile');
    });

    test('it logs out on logout button click', async () => {
        const apiSpy = jest.spyOn(WwcApi, 'logout').mockReturnValue(await Promise.resolve('hello'));
        const { getByText } = render(<ContainerWithNav />);
        const logoutButton = getByText(/Log Out/i);

        fireEvent.click(logoutButton);

        await expect(apiSpy).toHaveBeenCalledTimes(1);
        expect(mockHandleRemoveAuth).toHaveBeenCalledTimes(1);
        expect(mockNavigation).toBeCalledWith('/login');
        //done();
        return Promise.resolve()
    });
});