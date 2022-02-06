import React from 'react';
import BackButton from "../../images/arrow_back_24px.png";
import styles from "./BackToMemberPortal.module.css";
import { useHistory } from "react-router-dom";

const BackToMemberPortal = () => {
  const history = useHistory();
  return (
    <div>
      <button
        className={styles["back-member-btn"]}
        onClick={() => {
          history.push({ pathname: "/viewMembers" });
        }}
      >
        <img
        src={BackButton}
        className={styles["back-btn-img"]}
        alt="Back Button"
      />
      Back to Member Portal
      </button>
    </div>
  )
}

export default BackToMemberPortal;
