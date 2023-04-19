// THIS COMPONENT IS NOT USED AND CAN BE REMOVED.

import React from "react";
import classes from "./PasswordResetSuccessModal.module.css";

const PasswordResetSuccessModal = (props) => {
  return (
    <div
      className={`modal ${classes.bg} show`}
      id={classes.passwordResetSuccessModal}
      tabIndex='-1'
      role='dialog'
    >
      <div className='modal-dialog modal-dialog-centered'>
        <div className='modal-content'>
          <div className={`modal-header ${classes.header}`}>
            <button
              type='button'
              className='close'
              aria-label='Close'
              data-bs-dismiss='modal'
              onClick={props.close}
            >
              <span aria-hidden='true'>&times;</span>
            </button>
          </div>
          <div className={`modal-body ${classes.body}`}>
            <div className={classes.title}>Password Reset Successful</div>
            <div className={classes.bodyText}>
              {" "}
              You may now login with your new password
            </div>
            <div className='d-flex justify-content-center'>
              <button
                type='button'
                className={classes.btn}
                data-bs-dismiss='modal'
                onClick={props.close}
              >
                Close
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
export default PasswordResetSuccessModal;
