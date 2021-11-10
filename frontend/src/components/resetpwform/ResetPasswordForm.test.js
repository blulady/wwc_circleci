import React from "react";
import { render, screen, act, fireEvent } from "@testing-library/react";
import ConfirmResetPassword from "./ResetPasswordForm";
import AuthProvider from "../../context/auth/AuthProvider";
import WwcApi from "../../WwcApi";
import { createMemoryHistory } from 'history';
import { Router} from "react-router";

jest.mock("react-router");
jest.mock("../../WwcApi");

test('it should render reset password form', () => {
  const history = createMemoryHistory({initialEntries: ['/register?email=a@b.com&token=test']});
        let loc = {search: "?email=a@b.com&token=test"};
  const handleSetAuth = jest.fn();
  const { getByTestId } = render (
    <AuthProvider value={{handleSetAuth,}}> 
      <Router history={history}>
        <ConfirmResetPassword location={loc}/>
      </Router>
    </AuthProvider>
  )

  const resetPwForm = getByTestId("reset-pw-form")
  const resetPwBtn = getByTestId("reset-pw-button")

  expect(resetPwForm).toBeInTheDocument();  
  expect(resetPwBtn).toBeInTheDocument(); 
});