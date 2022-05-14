import React, { useState } from 'react'
import ContainerWithNav from "../layout/ContainerWithNav";
import styles from "./TeamHomeContainer.module.css";
import cx from "classnames";
import { NavLink, Outlet, useParams } from 'react-router-dom';
import { useTeamContext } from '../../context/team/TeamContext';

const paths = {
  "members": {
      "path": "/members"
  },
  "resources": {
      "path": "/resources"
  }
};

const TeamHomeContainer = (props) =>{
  const params = useParams();
  const team = parseInt(params.team);
  const { teams } = useTeamContext();
  const [currentPage, setCurrentPage] = useState(0); 
  
  const teamInfo = teams[team];

  return (
    <ContainerWithNav>
    <div
        id='teamHomeContainer'
        className={cx(styles["team-home-container"], "d-flex flex-column")}
       >
      <div className={styles["team-home-container-inner"]}>  
        <div className={styles["team-home-tab-container"] + " d-flex align-items-end"}>
          {
            teamInfo.pages.map((page, i) => (
              <button key={i} className={styles["tab-button"] + ((i === currentPage) ? " " + styles["tab-button-selected"] : '')} onClick={() => setCurrentPage(i)}>
                <NavLink to={"/team/" + team + paths[page.pageId].path}>{page.label}</NavLink>
              </button>
            ))
          }
        </div>
        <div
          className={cx(styles["team-home-tab-contents"], "d-flex flex-column")}
        >
          <Outlet />
        </div>
      </div>   
    </div>
    </ContainerWithNav>
  )
};
export default TeamHomeContainer;