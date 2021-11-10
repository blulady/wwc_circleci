import React from "react";
import { render, screen, act, fireEvent } from "@testing-library/react";
import ConfirmResetPassword from "./ResetPasswordForm";
import AuthProvider from "../../context/auth/AuthProvider";

jest.mock("react-router");
jest.mock("../../WwcApi");

test('it should render reset password form', () => {
  let loc = {search: "?email=a@b.com&token=test"};
  const handleSetAuth = jest.fn();
  const { getByTestId } = render (
    <AuthProvider value={{handleSetAuth,}}> 
      <ConfirmResetPassword location={loc}/>
    </AuthProvider>
  )

  const resetPwForm = getByTestId("reset-pw-form")
  const resetPwBtn = getByTestId("reset-pw-button")

  expect(resetPwForm).toBeInTheDocument();  
  expect(resetPwBtn).toBeInTheDocument(); 
});