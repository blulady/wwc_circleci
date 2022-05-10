import React from 'react';
import styles from "./ChapterMembersButton.module.css";
import { useNavigate } from "react-router-dom";


const ChapterMembersButton = () => {
  const navigate = useNavigate();
  
  return (
    <div>
    <button
      className={styles['tab-selected-button']}
      onClick={() => {
        navigate("/members/chaptermembers");
      }}
    >
      Chapter Members
    </button>
  </div>
  )
}

export default ChapterMembersButton;
