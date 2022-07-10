import React from 'react'
import cx from "classnames";
import styles from "./UserProfile.module.css";
import classes from "../memberdetails/MemberDetails.module.css";

const UserName = ({firstName, lastName, showEditModal}) => {

  return (<React.Fragment>
      <div className={styles["fullname-font"]}>
        {firstName + " " + lastName}
      </div>
      <span
        id="name-edit"
        data-testid='change-name-icon'
        className={classes["icon-wrapper"]}
        onClick={showEditModal}
        >
            <i
            className={cx(
                "fas fa-pen",
                styles["name-edit-icon"],
                classes["member-info-icon", "member-icon-active"])}
            ></i>
        </span>
  </React.Fragment>)

}

export default UserName
