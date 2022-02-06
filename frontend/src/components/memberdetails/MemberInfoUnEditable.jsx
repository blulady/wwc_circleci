import React from 'react'
import styles from "./MemberInfoUnEditable.module.css";

const MemberInfoUnEditable = ({first_name, last_name, email, date_joined}) => {

  const formatDate = (dateStr) => {
    if (!dateStr) {
      return "";
    }
    let d = new Date(dateStr);
    const options = { year: "numeric", month: "long", day: "numeric" };
    return d.toLocaleDateString("en-US", options);
  };
  return (
    <div className={styles["view-member-name-email-date"]}>
      <div className={styles["fullname-font"]}>
        {first_name + " " + last_name}
      </div>
      <div className={styles["email-font"]}>{email}</div>
      <div className={styles["datejoined-font"]}>
        {"Member Since " + formatDate(date_joined)}
      </div>
    </div>
  )
}

export default MemberInfoUnEditable
