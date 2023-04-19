// THIS COMPONENT IS NOT USED AND CAN BE REMOVED.

import React from "react";

const ResetModal = (props) => {
  return (
    <div
      className="modal modal-success-bg show"
      id="ResetModal"
      tabIndex="-1"
      role="dialog"
    >
      <div className="modal-dialog modal-dialog-centered">
        <div className="modal-content">
          <div className="modal-header modal-success-header">
            <button
              type="button"
              className="close"
              aria-label="Close"
              data-bs-dismiss="modal"
              close={props.close}
            >
              <span aria-hidden="true">&times;</span>
            </button>
          </div>
          <div className="modal-body modal-success-body">
            <div className="modal-success-title">Password reset succesful</div>
            <div className="modal-success-body-text">
              {" "}
              You may now login with your new password
            </div>
            <div className="d-flex justify-content-center">
              <button
                type="button"
                className="modal-success-btn"
                data-bs-dismiss="modal"
                onClick={props.onClick}
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
export default ResetModal;
