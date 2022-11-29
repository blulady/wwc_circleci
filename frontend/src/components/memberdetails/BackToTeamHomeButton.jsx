import React from 'react';
import styles from "./BackToTeamHomeButton.module.css";
import { useNavigate } from "react-router-dom";
import { useTeamContext } from '../../context/team/TeamContext';


const BackToTeamHomeButton = ({teamId}) => {
  const navigate = useNavigate();
  const { teams } = useTeamContext();
  const teamInfo = teams[teamId];
  const teamHome = teamInfo.pages[0].label;
  
  return (
    <div>
    <button
      className={styles['tab-selected-button']}
      onClick={() => {
        navigate("/team/" + teamId +"/members");
      }}
    >
      {teamHome}
    </button>
  </div>
  )
}

export default BackToTeamHomeButton;
