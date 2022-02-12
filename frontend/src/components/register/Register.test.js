import React from 'react';
import { act, render, screen } from '@testing-library/react';
import Register from './Register';
import { createMemoryHistory } from 'history';
import { Router} from "react-router";
import WwcApi from "../../WwcApi";


jest.mock("../../WwcApi", () => {
  return {
    ...jest.requireActual("../../WwcApi"),
    validateInvitation: jest.fn(),
    activateMember: jest.fn()
  };
});


describe('Register Component Validation Tests', () =>{
  const history = createMemoryHistory({initialEntries: ['/register?email=a@b.com&token=test']});
  let loc;
  
  beforeEach(() => {
    jest.resetAllMocks();
    loc = {search: "?email=a@b.com&token=test"};
  });

  test('Tests Register component behavior for VALID invitation', async () => {    
    // Mock VALID invitation
    WwcApi.validateInvitation.mockImplementation( 
      async () => {
        return await Promise.resolve({
            data: {
              success: {
                  status: "VALID",
                  message: "Toke is valid"
              }
            }
        })
      }
    );
    // Mock successful activation
    WwcApi.activateMember.mockImplementation( 
      async () => {
        return await Promise.resolve({
            data: {
              result: "User Activated Successfully"
            }
        })
      }
    );
    await act(async () => {
      render(
        <Router history={history}>
          <Register location={loc}/>
        </Router>
      );
    });
    // Registration form is rendered
    const emailInp = screen.getByTestId('register-email');
    const submitBtn = screen.getByTestId('register-submit-button');
    expect(screen.getByText(/Register for/i)).toBeInTheDocument();
    expect(screen.getByText(/Chapter Tools/i)).toBeInTheDocument();
    expect(emailInp).toBeInTheDocument();
    expect(emailInp).toHaveAttribute('readOnly');
    expect(emailInp).toHaveAttribute('value','a@b.com');
    expect(submitBtn).toBeInTheDocument();
    expect(submitBtn).toHaveAttribute('disabled');
  });

  test('Tests Register component behavior for USED invitation', async () => {    
    // Mock USED invitation
    WwcApi.validateInvitation.mockImplementation( 
      async () => {
        return await Promise.resolve({
            data: {
              success: {
                  status: "USED",
                  message: "Token is already used"
              }
            }
        })}
      );
    await act(async () => {
      render(
        <Router history={history}>
          <Register location={loc}/>
        </Router>
      );
    });
    // Error message is rendered
    const msgBox = screen.getByTestId('message-box');
    expect(screen.getByText(/Oops/i)).toBeInTheDocument();
    expect(screen.getByText(/This link has already been used/i)).toBeInTheDocument();
    expect(msgBox).toBeInTheDocument();
  });

  test('Tests Register component behavior for EXPIRED invitation', async () => {       
    // Mock EXPIRED invitation
    WwcApi.validateInvitation.mockImplementation( 
      async () => {
        return await Promise.resolve({
            data: {
              success: {
                  status: "EXPIRED",
                  message: "Token has expired"
              }
            }
        })}
      );
    await act(async () => {
      render(
        <Router history={history}>
          <Register location={loc}/>
        </Router>
      );
    });
    // Error message is rendered
    const msgBox = screen.getByTestId('message-box');
    expect(screen.getByText(/Oops/i)).toBeInTheDocument();
    expect(screen.getByText(/This link has expired/i)).toBeInTheDocument();
    expect(msgBox).toBeInTheDocument();
  });

  test('Tests Register component behavior for ERROR with invitation', async () => {       
    // Mock ERROR with invitation
    WwcApi.validateInvitation.mockImplementation( 
      async () => {
        return await Promise.reject({
            data: {
              detail: "Not found."
            }
        })}
      );
    await act(async () => {
      render(
        <Router history={history}>
          <Register location={loc}/>
        </Router>
      );
    });
    // Error message is rendered
    const msgBox = screen.getByTestId('message-box');
    expect(screen.getByText(/Sorry/i)).toBeInTheDocument();
    expect(screen.getByText(/We could not process your request/i)).toBeInTheDocument();
    expect(msgBox).toBeInTheDocument();
  });

});
