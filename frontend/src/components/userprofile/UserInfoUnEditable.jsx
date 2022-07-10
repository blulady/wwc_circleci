import React from 'react'
import styles from "./UserProfile.module.css";

const MemberInfoUnEditable = ({email, date_joined}) => {

  const formatDate = (dateStr) => {
    if (!dateStr) {
      return "";
    }
    let d = new Date(dateStr);
    const options = { year: "numeric", month: "long", day: "numeric" };
    return d.toLocaleDateString("en-US", options);
  };
  return (
    <React.Fragment>
      <div className={styles["email-font"]}>{email}</div>
      <div className={styles["datejoined-font"]}>
        {"Member Since " + formatDate(date_joined)}
      </div>
    </React.Fragment>
  )
}

export default MemberInfoUnEditable
