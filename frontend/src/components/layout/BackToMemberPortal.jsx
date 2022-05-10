import React from 'react';
import BackButton from "../../images/arrow_back_24px.png";
import styles from "./BackToMemberPortal.module.css";
import { useNavigate } from "react-router-dom";

const BackToMemberPortal = () => {
  const navigate = useNavigate();
  return (
    <div>
      <button
        className={styles["back-member-btn"]}
        onClick={() => {
          navigate("/home");
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
