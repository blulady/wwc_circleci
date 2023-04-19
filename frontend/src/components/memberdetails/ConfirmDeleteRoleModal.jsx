import React from 'react';
import styles from "./ConfirmDeleteRoleModal.module.css";
import cx from "classnames";

const ConfirmDeleteRoleModal = ({role, deleteRole, closeModal}) => {

  const handleSubmit = (e) => {
    deleteRole();
  }

  const handleClose = () => {
    closeModal();
  }

  return (

      <div id="delete-role-modal" className={cx("modal show", styles["delete-role-modal"], styles["bg"])} tabIndex="-1" role="dialog" aria-labelledby="deleterolemodal" aria-hidden="true">
        <div className="modal-dialog modal-dialog-centered" role="document">
          <div className={cx("modal-content", styles["role-modal-content"])}>
            <div className="modal-header">
              <h5 className={cx("modal-title", styles["modal-confirmation"])}>Are you sure?</h5>
              <button type="button" className="close" aria-label="Close" onClick={handleClose}>
                <span aria-hidden="true">&times;</span>
              </button>
            </div>
            <div className={cx("modal-body", styles["modal-message"])}>
              <p>Are you sure you want to remove the <strong>{role}</strong> role and its associated teams?</p>
            </div>
            <div className="modal-footer d-flex justify-content-center">
              <button type="button" className={cx("btn btn-primary", styles["modal-submit"])} onClick={handleSubmit} data-bs-dismiss="modal">Confirm</button>
            </div>
          </div>
        </div>
      </div>
  )
}

export default ConfirmDeleteRoleModal
