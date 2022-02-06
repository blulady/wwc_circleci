import React, { useState, useEffect } from "react";
import styles from "./ViewMembers.module.css";
import cx from "classnames";
//import WwcApi from "../../WwcApi";
import MessageBox from "../messagebox/MessageBox";

import { ERROR_VOLUNTEER_RESOURCES_DOCUMENT_NOT_LOADED } from "../../Messages";
import { ERROR_VOLUNTEER_RESOURCES_NO_DOCUMENT_AVAILABLE } from "../../Messages";

const VolunteerResources = (props) => {

  const errorTitle = 'Sorry!';
  // FIXME: This is temp to avoid lint warnings for now
/*   const [errorOnLoading, setErrorOnLoading] = useState(false);
  const [errorNoDocument, setErrorNoDocument] = useState(false); */
  const [errorOnLoading] = useState(false);
  const [errorNoDocument] = useState(false);
  const [volunteerResource, setVolunteerResource] = useState({
    edit_link: "",
    published_link: ""
  });

  useEffect(() => {
    //  UnComment below code line,once the backend  code is deployed on heroku dev env
    // getVolunteerResources(slug);

    //testing : hardcoding the resource url; clean up once backend code available 
    setVolunteerResource({
      edit_link: "",
      published_link: "https://docs.google.com/document/d/e/2PACX-1vTCz0hr1N2DkTwpc3sJzuWwKlIX2HgzD-9OjOMBgJCSfizIQv0LecMdV7VdqLL4Mw0OGbTsGrWFpIm6/pub?embedded=true"
    })
  }, []);

/*   const getVolunteerResources = async (slug) => {
    try {
      let volunteerResources = await WwcApi.getVolunteerResources(slug);
      setVolunteerResource(volunteerResources)
      console.log(volunteerResource.published_link)
    } catch (error) {
      console.log(error);
      if (error.response.status === 404) {
        setErrorNoDocument(true);
      } else
        setErrorOnLoading(true);
    }
  }; */
  return (
    <div id='volunteerResourcesPage'
      className={cx(styles["view-member-page"], "d-flex flex-column")}
    >
      <div className={styles["view-member-page-list-wrapper"]}>
        <div className={styles["page-label-wrapper"]}>
          {" "}
        </div>
        {errorOnLoading && (
          <div className={cx(styles["error-container"], "d-flex justify-content-center")}>
            <MessageBox type="Error" title={errorTitle} message={ERROR_VOLUNTEER_RESOURCES_DOCUMENT_NOT_LOADED}></MessageBox>
          </div>
        )}
        {errorNoDocument && (
          <div className={cx(styles["error-container"], "d-flex justify-content-center")}>
            <MessageBox type="Error" title={errorTitle} message={ERROR_VOLUNTEER_RESOURCES_NO_DOCUMENT_AVAILABLE}></MessageBox>
          </div>
        )}
        {!errorNoDocument && !errorOnLoading && (
          <iframe style={{ width: '100%', height: '100%', background: "#FFFFFF", margin: 0, padding: 0, border: 'none' }}
            src={volunteerResource.published_link} title="Volunteer Resources">
          </iframe>
        )}
      </div>
    </div>
  );
};
export default VolunteerResources;