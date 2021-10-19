import React from 'react';
import { render, fireEvent, act } from '@testing-library/react';
import Password from './Password';

const mockSetPassword = jest.fn();

describe('Password', () => {
    beforeEach(() => {
        mockSetPassword.mockClear(); 
    });

    test('it renders without crashing', () => {
        const { container } = render(<Password setPwd={mockSetPassword} />);
        expect(container).toMatchSnapshot();
    });

    test('it validates password on change', () => {
        const mockSetPwdValidation = jest.fn();
        const passwordSpy = jest.spyOn(React, 'useState').mockImplementation((init) => {
            return [init, mockSetPwdValidation];
        });

        const { container, getByTestId } = render(<Password setPwd={mockSetPassword} />);
        const inputPwd = getByTestId('password');
        inputPwd.value = "Password123";

        setTimeout(() => {
            expect(mockSetPwdValidation).toBeCalledWith([true, true, true, true]);
        }, 100);
    });

    test('it shows password on show button click', () => {
        const { container, getByTestId } = render(<Password setPwd={mockSetPassword} />);
        const inputPwd = getByTestId('password');
        const showHide = getByTestId('show-hide');

        fireEvent.click(showHide);

        expect(inputPwd.type).toBe('text');
    });
});