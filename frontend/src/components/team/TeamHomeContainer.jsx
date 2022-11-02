import React, { useState, useContext } from 'react'
import ContainerWithNav from "../layout/ContainerWithNav";
import styles from "./TeamHomeContainer.module.css";
import cx from "classnames";
import { NavLink, Outlet, useParams, useLocation } from 'react-router-dom';
import { useTeamContext } from '../../context/team/TeamContext';
import AuthContext from "../../context/auth/AuthContext";

const TeamHomeContainer = (props) => {
  const params = useParams();
  const team = parseInt(params.team);
  const { teams } = useTeamContext();
  const teamInfo = teams[team];
  const location = useLocation();
  let pageId = 0;
  teamInfo.pages.forEach((p, index) => {
    if (location.pathname.indexOf(p.pageId) > -1) {
      pageId = index;
    }
  });
  const [currentPage, setCurrentPage] = useState(pageId);



  const { userInfo } = useContext(AuthContext);
  const isDirector = userInfo.role === "DIRECTOR";

  return (
    <ContainerWithNav>
      <div
        id='teamHomeContainer'
        className={cx(styles["team-home-container"], "d-flex flex-column")}
      >
        <div className={styles["team-home-container-inner"]}>
          <div className={styles["team-home-tab-container"] + " d-flex align-items-end"}>
            {
              teamInfo.pages.map((page, i) => {
                if (!page.isDirectorOnly || isDirector) {
                  return (
                  
                    <NavLink to={"/team/" + team + "/" + page.pageId} key={i}>
                      <button className={styles["tab-button"] + ((i === currentPage) ? " " + styles["tab-button-selected"] : '')} onClick={() => setCurrentPage(i)}>
                        {page.label}</button></NavLink>
                  )
                }
              }
              )
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