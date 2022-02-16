import React from 'react';
import styles from "./MemberDetails.module.css";
import classes from "./MemberStatus.module.css";
import cx from "classnames";

const MemberStatus = ({status, changeStatus=null}) => {

  const handleStatusChange = (e) => {
    changeStatus(e.target.checked);
  }

  return (
    <>
      <section className={styles["section-box"]}>
        <div className={styles["col-wrapper"]}>
          <div className={styles["label-font"]}>Status:</div>
          <div className={classes["status-icon-wrapper"]}>
            <i className={cx("fas fa-star", classes["status-icon"] , status === 'ACTIVE' ? classes["status-icon-active"]: classes["status-icon-inactive"])}></i>
          </div>

          <div className={styles["member-info-text"]}>
            {status.toLowerCase()}
          </div>
        </div>
        {status === "PENDING" || !changeStatus ? (
          ""
        ) : (
          <div className={classes["change-status-wrapper"]}>
            <label className={classes["switch"]}>
              <input className={classes["switch-input"]} type="checkbox" checked={status==="ACTIVE" ? 'checked' : ''} onChange={handleStatusChange} data-testid="change-status-btn"/>
              <span className={cx(classes["switch-slider"], classes["switch-round"])}></span>
            </label>
            <p className={styles["change-status-text"]}>Change Status</p>
          </div>
        )}
      </section>
      <hr className={styles["section-divider"]} />
    </>
  )
}

export default MemberStatus
