// THIS COMPONENT IS NOT USED AND CAN BE REMOVED.

import React from "react";
import classes from "./RequestSentModal.module.css";

const RequestSentModal = (props) => {
  return (
    <div
      className={`modal ${classes.bg} show`}
      id={classes.requestSentModal}
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
            <div className={classes.title}>Request sent</div>
            <div className={classes.bodyText}>
              {" "}
              Please check your email inbox for password reset instructions
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
export default RequestSentModal;
