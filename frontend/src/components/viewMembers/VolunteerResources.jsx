import React from "react";
import styles from "./ViewMembers.module.css";
import cx from "classnames";


const VolunteerResources = (props) => {  
  return (
    <div id='volunteerResourcesPage'
      className={cx(styles["view-member-page"], "d-flex flex-column")}
    >    
        <div className={styles["view-member-page-list-wrapper"]}>
          <div className={styles["page-label-wrapper"]}>
            {" "}
          </div>
         <iframe style={{ width: '100%', height: '100%', background: "#FFFFFF;", margin: 0, padding: 0, border: 'none' }}
            src="https://docs.google.com/document/d/e/2PACX-1vTCz0hr1N2DkTwpc3sJzuWwKlIX2HgzD-9OjOMBgJCSfizIQv0LecMdV7VdqLL4Mw0OGbTsGrWFpIm6/pub?embedded=true">
          </iframe>
        </div>
    </div>

  );
};
export default VolunteerResources;