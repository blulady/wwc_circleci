import React, { useState } from "react";
import WwcBackground from "./WwcBackground";
import classes from "./ResetPasswordModal.module.css";

const ResetPasswordModal = (props) => {
  const [emailData, setEmailData] = useState({
    email: "",
  });

  /*
   * on submit sets success state to true
   * stores token in session
   * and redirects to logout page
   */
  const handleSubmit = (event) => {
    event.preventDefault();
    props.send(emailData);
  };

  // updates email state
  const handleChange = (event) => {
    let nam = event.target.name;
    let val = event.target.value;
    setEmailData({ [nam]: val });
  };

  return (
    <div className='modal show' tabIndex='-1'>
      <div>
        <WwcBackground>
          <div className={classes.BackgroundOpacity}></div>
          <div className='container'>
            <div className='WwcLogo'></div>
            <main>
              <div className='modal-dialog modal-dialog-centered'>
                <div
                  className={`modal-content ${classes.content} ${classes.dialog}`}
                >
                  <div className='header'>
                    <div className={classes.h3}>Reset your password</div>
                  </div>
                  <div className={classes.body}>
                    Enter your email address and we will send you reset
                    instructions
                  </div>
                  <form
                    className='needs-validation mb-4'
                    onSubmit={handleSubmit}
                  >
                    <div className='invalid-feedback'>Invalid email</div>
                    <div className={`form-group ${classes.form}`}>
                      <label className='label' htmlFor='reset-email'>
                        Email
                      </label>
                      <input
                        type='email'
                        pattern='[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,4}$'
                        name='email'
                        id='reset-email'
                        className='form-control'
                        required
                        onChange={handleChange}
                      />
                    </div>
                    <div className='d-flex justify-content-center'>
                      <button
                        type='submit'
                        className='modal-confirm-btn m-auto'
                      >
                        Reset
                      </button>
                    </div>
                  </form>
                  <div className='d-flex justify-content-center'>
                    <button className='hypertext' onClick={props.close}>
                      Back to Login
                    </button>
                  </div>
                </div>
              </div>
            </main>
          </div>
        </WwcBackground>
      </div>
    </div>
  );
};

export default ResetPasswordModal;
