import React from 'react';
import { render, fireEvent, act } from '@testing-library/react';
import ConfirmationModal from './ConfirmationModal';
import EmailInput from './EmailInput';
import InputLabel from './InputLabel';
import RoleRadioField from './RoleRadioField';
import SuccessModal from './SuccessModal';
import TextAreaInput from './TextAreaInput';

describe('ConfirmationModal', () => {
    const mockShowModal = jest.fn();

    test('it renders without crashing', () => {
        const { container } = render(<ConfirmationModal memberrole='Volunteer'
                                                        memberdesc='Limited access to areas of portal'
                                                        onClick={mockShowModal} />);
        
        expect(container).toMatchSnapshot();
    });

    test('it calls onClick handler on confirmation click', () => {
        const { container } = render(<ConfirmationModal memberrole='Volunteer'
                                                        memberdesc='Limited access to areas of portal'
                                                        onClick={mockShowModal} />);
        const button = container.querySelector('.modal-confirm-btn');

        act(() => {
            fireEvent.click(button);
        });

        expect(mockShowModal).toHaveBeenCalledTimes(1);
    });
});

describe('EmailInput', () => {
    const mockHandleChange = jest.fn();

    test('it renders without crashing', () => {
        const { container } = render(<EmailInput name='Email'
                                                 className='form-control email-input'
                                                 pclass='hide'
                                                 editclass='hide'
                                                 buttonclass='hide'
                                                 onChange={mockHandleChange}
                                                 placeholder='eg. sam@wwcode.com' />);
        
        expect(container).toMatchSnapshot();
    });

    test('it calls onChange handler on input change', () => {
        const { container } = render(<EmailInput name='Email'
                                                 className='form-control email-input'
                                                 pclass='hide'
                                                 editclass='hide'
                                                 buttonclass='hide'
                                                 onChange={mockHandleChange}
                                                 placeholder='eg. sam@wwcode.com' />);
        const input = container.querySelector('.email-input');

        act(() => {
            fireEvent.change(input, { target: { value: 'test@example.com' } });
        });
        
        expect(mockHandleChange).toHaveBeenCalledTimes(1);
        expect(input.value).toBe('test@example.com');
    });
});

describe('InputLabel', () => {
    test('it renders without crashing', () => {
        const { container } = render(<InputLabel labelname='test' text='hello world!' />);
        
        expect(container).toMatchSnapshot();
    });
});

describe('RoleRadioField', () => {
    const mockHandleClick = jest.fn();
    const mockHandleChange = jest.fn();

    test('it renders without crashing', () => {
        const { container } = render(<RoleRadioField className='form-check-input position-static role-radio'
                                                     id='1'
                                                     name='Role'
                                                     value='Volunteer'
                                                     pclass='hide'
                                                     datatarget='#confirmModal'
                                                     onClick={mockHandleClick}
                                                     onChange={mockHandleChange}
                                                     roletext='Volunteer'
                                                     roledesc='Limited access to areas of portal' />);
        
        expect(container).toMatchSnapshot();
    });

    test('it calls onClick handler on input click', () => {
        const { container } = render(<RoleRadioField className='form-check-input position-static role-radio'
                                                     id='1'
                                                     name='Role'
                                                     value='Volunteer'
                                                     pclass='hide'
                                                     datatarget='#confirmModal'
                                                     onClick={mockHandleClick}
                                                     onChange={mockHandleChange}
                                                     roletext='Volunteer'
                                                     roledesc='Limited access to areas of portal' />);
        const input = container.querySelector('.role-radio');
                                                
        act(() => {
            fireEvent.click(input);
        });

        expect(mockHandleClick).toHaveBeenCalledTimes(1);
    });
});

describe('SuccessModal', () => {
    const mockHandleClick = jest.fn();

    test('it renders without crashing', () => {
        const { container } = render(<SuccessModal onClick={mockHandleClick} />);
        
        expect(container).toMatchSnapshot();
    });

    test('it calls onClick handler on button click', () => {
        const { container } = render(<SuccessModal onClick={mockHandleClick} />);
        const button = container.querySelector('.modal-success-btn');

        act(() => {
            fireEvent.click(button);
        });

        expect(mockHandleClick).toHaveBeenCalledTimes(1);
    });
});

describe('TextAreaInput', () => {
    let mockMessage = "Hello World!";
    let mockCounterValue = mockMessage.length;
    const mockHandleChange = jest.fn();
    
    test('it renders without crashing', () => {
        const { container } = render(<TextAreaInput name='Message'
                                                    pclass='hide'
                                                    editclass='hide'
                                                    buttonclass='hide'
                                                    className='form-control message-textarea'
                                                    onChange={mockHandleChange}
                                                    counterclass='message-counter'
                                                    value={mockMessage}
                                                    countervalue={mockCounterValue} />);
        
        expect(container).toMatchSnapshot();
    });

    test('it calls onChange handler on textarea change', () => {
        const { container } = render(<TextAreaInput name='Message'
                                                    pclass='hide'
                                                    editclass='hide'
                                                    buttonclass='hide'
                                                    className='form-control message-textarea'
                                                    onChange={mockHandleChange}
                                                    counterclass='message-counter'
                                                    value={mockMessage}
                                                    countervalue={mockCounterValue} />);
        const textArea = container.querySelector('.message-textarea');
        const counter = container.querySelector('.message-counter');
        mockMessage = 'Hello There!'
        mockCounterValue = mockMessage.length;

        act(() => {
            fireEvent.change(textArea, { target: { value: mockMessage } });
        });

        setTimeout(() => {
            expect(mockHandleChange).toHaveBeenCalledTimes(1);
            expect(textArea.value).toBe('Hello There!');
            expect(counter).toHaveTextContent(7);
        });
    });
});