import React from "react";

const ConfirmationModal = (props) => {
  return (
    <div className="modal" id="confirmModal" tabIndex="-1" role="dialog">
      <div className="modal-dialog">
        <div className="modal-content">
          <div className="modal-body modal-open-text">
            *Selected role for this member is{" "}
            <span className="confirm-message">{props.memberrole}</span>, who
            will have{" "}
            <span className="confirm-message">{props.memberdesc}</span>
            <div className="d-flex justify-content-center">
              <button
                type="button"
                className="modal-confirm-btn"
                data-dismiss="modal"
                onClick={props.onClick}
              >
                Confirm
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
export default ConfirmationModal;
