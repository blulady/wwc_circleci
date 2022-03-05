import React, {useState} from 'react';
import ConfirmDeleteRoleModal from "./ConfirmDeleteRoleModal";

import styles from "./MemberDetails.module.css";
import cx from "classnames";

const MemberRole = ({role, status, numRoles, modifyRole = null}) => {

  const [showModal, setShowModal] = useState(false);

  const handleIconClick = () => {
    setShowModal(true);
  }

  const handleDeleteRole = () => {
    setShowModal(false);
    modifyRole(role);
    //Todo: API call to delete role
  }

  const handleCloseRoleModal = () => {
    setShowModal(false);
  }

  return (
    <section className={styles["section-box"]}>
        <div className={styles["col-wrapper"]}>
          <div className={styles["label-font"]}>Role:</div>
          <div className={styles["member-info-text"]}>
            {role?.toLowerCase()}
          </div>
        </div>
        {/* TODO: Enable remove once BE is ready */}
        {/* <div id="role-delete" className={styles["icon-wrapper"]} onClick={status === 'ACTIVE' && numRoles>1 ? handleIconClick : null}>
          {status === "PENDING" || !modifyRole ? (
            ""
          ) : (
            <>
            <i className={cx("fas fa-trash",styles['member-info-icon'] ,status === 'ACTIVE' && numRoles>1 ? styles["member-icon-active"]: styles["member-icon-inactive"])}></i>
            <p className={styles["change-status-text"]}>Remove Role</p>
            </>
          )}
        </div> */}
        {showModal? <ConfirmDeleteRoleModal role={role}  deleteRole={handleDeleteRole} closeModal={handleCloseRoleModal}/> : null }
      </section>
  )
}

export default MemberRole
