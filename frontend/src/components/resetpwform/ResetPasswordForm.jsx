import React, { useState } from "react";
import { Redirect } from "react-router-dom";
import queryString from "query-string";
import Password from "../layout/Password"
import classes from "./ResetPasswordForm.module.css";
import ContainerWithNav from "../layout/ContainerWithNav";
import WwcApi from "../../WwcApi";


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
  try {
    await WwcApi.resetPassword(data);
    sessionStorage.setItem('password-reset', true);
  } catch (error) {
    alert(error.response.data.error);
  }
  setSubmitted(true);

 
};

return submitted 
  ? <Redirect to="/login" /> 
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
