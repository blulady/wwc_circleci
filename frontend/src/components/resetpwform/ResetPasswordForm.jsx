import React, { useState } from "react";
import { Navigate } from "react-router-dom";
import queryString from "query-string";
import Password from "../layout/Password"
import classes from "./ResetPasswordForm.module.css";
import ContainerWithNav from "../layout/ContainerWithNav";
import WwcApi from "../../WwcApi";
import { ERROR_REQUEST_MESSAGE, SUCCESS_PASSWORD_RESET } from "../../Messages";


const ConfirmResetPassword = (props) => {
  const { email, token } = queryString.parse(props.location.search);
  const [submitted,setSubmitted] = useState(false);
  const [password, setPassword] = useState("");

  const handleSetPassword = (pwd) => {
    setPassword(pwd);
  }
 // function to handle form submission
 const handleSubmit = async (e) => {
  e.preventDefault();
  let data = {email,token,password};
  let passwordResetInfo;
  try {
    await WwcApi.resetPassword(data);
    passwordResetInfo = {type: "Success",
                               title: "Password Reset Successful",
                               message: SUCCESS_PASSWORD_RESET};
  } catch (error) {
    passwordResetInfo = {type: "Error", 
                         title: "Sorry!",
                         message: ERROR_REQUEST_MESSAGE};
  }
  sessionStorage.setItem('password-reset', JSON.stringify(passwordResetInfo));
  setSubmitted(true);
};

return submitted 
  ? <Navigate to="/login" /> 
  :(
    <ContainerWithNav>
        <div className={`${classes.ResetPassword} col col-md-6 col-lg-4`}>
          <header>
            <div className={classes.title}>Reset your password</div>
          </header>
          <div className={classes.passwordForm}>
            <form onSubmit={handleSubmit} data-testid='reset-pw-form'>
              <Password setPwd={handleSetPassword} pwdLabel="Enter New Password" />
              <div className='text-center'>
                <button
                  type='submit'
                  className={`btn ${classes.btn}`}
                  disabled={
                    !password 
                  }
                  data-testid='reset-pw-button'
                >
                  Reset
                </button>
              </div>
            </form>
          </div>
        </div>
    </ContainerWithNav>
  );
};

export default ConfirmResetPassword;
