import React from 'react';
import { render, fireEvent } from '@testing-library/react';
import AddMember from './AddMember';

const mockHistoryPush = jest.fn();
let mockFromReview = false;

jest.mock('react-router-dom', () => {
    const ActualReactRouterDom = require.requireActual('react-router-dom');
    return {
        ...ActualReactRouterDom,
        useHistory: () => ({
        push: mockHistoryPush,
        replace: jest.fn()
        }),
        useLocation: () => ({
            state: {
                fromReview: mockFromReview
            }
        })
    }
});

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
    };
});

describe('AddMember', () => {
    test('it renders without crashing', () => {
        const { container } = render(<AddMember />);
        
        expect(container).toMatchSnapshot();
    });

    test('it reflects input change', () => {
        const { container, rerender } = render(<AddMember />);
        const emailInput = container.querySelector('.email-input');
        const selectedRole = container.querySelector("[id='2']");
        const textAreaInput = container.querySelector('.message-textarea');

        fireEvent.change(emailInput, { target: { value: 'test@example.com' } });
        fireEvent.click(selectedRole);
        fireEvent.change(textAreaInput, { target: { value: 'hello world!' } });
        rerender();

        expect(emailInput.value).toBe('test@example.com');
        expect(selectedRole).toHaveClass('role-radio-selected');
        expect(textAreaInput.value).toBe('hello world!');
    });

    test('it handles form submit', () => {
        const { container, getByText } = render(<AddMember />);
        const emailInput = container.querySelector('.email-input');
        const selectedRole = container.querySelector("[id='3']");
        const textAreaInput = container.querySelector('.message-textarea');

        fireEvent.change(emailInput, { target: { value: 'test@example.com' } });
        fireEvent.click(selectedRole);
        fireEvent.change(textAreaInput, { target: { value: 'hello world!' } });
        fireEvent.click(getByText('Confirm'));
        fireEvent.submit(getByText('Review'));

        expect(mockHistoryPush).toHaveBeenCalledTimes(1);
    });


    test('it shows success modal', () => {
        mockFromReview = true;
        const { getByText } = render(<AddMember />);

        expect(getByText('Member has been added and emailed a registration link')).toBeInTheDocument();
    });
});