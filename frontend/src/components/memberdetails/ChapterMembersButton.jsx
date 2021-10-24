import React from 'react';
import styles from "./ChapterMembersButton.module.css";
import { useHistory } from "react-router-dom";


const ChapterMembersButton = () => {
  const history = useHistory();
  
  return (
    <div>
    <button
      className={styles['tab-selected-button']}
      onClick={() => {
        history.push({ pathname: "/members/chaptermembers" });
      }}
    >
      Chapter Members
    </button>
  </div>
  )
}

export default ChapterMembersButton;
