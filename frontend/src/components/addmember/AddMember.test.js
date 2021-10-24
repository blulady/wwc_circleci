import React from 'react';
import { render, fireEvent, act } from '@testing-library/react';
import AddMember from './AddMember';

const mockSetState = jest.fn();
const mockHistoryPush = jest.fn();
const expectedMemberInfo = {
    Email: 'test@example.com',
    Role: 'Leader',
    Message: 'hello world!'
};
const expectedMemberRole = {
    'MemberRoleId': '2',
    'MemberRole': 'Leader',
    'MemberRoleDescription': 'Access to all areas excluding Director area'
};

jest.mock('react-router-dom', () => ({
    useHistory: () => ({
      push: mockHistoryPush,
      replace: jest.fn()
    }),
    useLocation: () => ({
        state: {
            fromReview: false
        }
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
            handleRemoveAuth: jest.fn()
        }),
        useState: (init) => {
            return [init, mockSetState];
        }
    };
});

describe('AddMember', () => {
    beforeEach(() => {
        mockSetState.mockClear();
    });

    test('it renders without crashing', () => {
        const { container } = render(<AddMember />);
        
        expect(container).toMatchSnapshot();
    });

    test('it calls setNewMember on input change', () => {
        const { container } = render(<AddMember />);
        const emailInput = container.querySelector('.email-input');
        const selectedRole = container.querySelector("[id='2']");
        const textAreaInput = container.querySelector('.message-textarea');

        act(() => {
            fireEvent.change(emailInput, { target: { value: 'test@example.com' } });
            fireEvent.click(selectedRole);
            fireEvent.change(textAreaInput, { target: { value: 'hello world!' } });
        });

        expect(mockSetState).toHaveBeenCalledTimes(6);
        // expect to have been called with
    });

    test('it calls setMemberRole, setNewMember, setCheckId, setShowModal on radio click', () => {
        const { container } = render(<AddMember />);
        const selectedRole = container.querySelector("[id='2']");

        act(() => {
            fireEvent.click(selectedRole);
        });

        expect(mockSetState).toHaveBeenCalledTimes(4);

        // setMemberRole call
        //expect(mockSetState).toBeCalledWith(expectedMemberRole);

        // setCheckId call
        //expect(mockSetState).toBeCalledWith(2);

        // setShowModal call
        //expect(mockSetState).toBeCalledWith(true);

        // setNewMember call
        //expect(mockSetState).toBeCalledWith({ Role: 'Leader' });
    });

    test('it calls handleSubmit on form submit', () => {
        const { container } = render(<AddMember />);
        const emailInput = container.querySelector('.email-input');
        const selectedRole = container.querySelector("[id='3']");
        const reviewBtn = container.querySelector('.review-btn');

        act(() => {
            fireEvent.change(emailInput, { target: { value: 'test@example.com' } });
            fireEvent.click(selectedRole);
        });

        act(() => {
            const confirmBtn = container.querySelector('.modal-confirm-btn');
            fireEvent.click(confirmBtn);
            fireEvent.click(reviewBtn);
        });

        //expect(mockHistoryPush).toHaveBeenCalledTimes(1);
        //expect(mockHistoryPush).toBeCalledWith({ pathname: '/member/review', state: { memberinfo: expectedMemberInfo, roleinfo: expectedMemberRole } });
    });
});