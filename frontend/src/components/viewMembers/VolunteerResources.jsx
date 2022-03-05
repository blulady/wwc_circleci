import React, { useState, useEffect, useContext } from "react";
import AuthContext from "../../context/auth/AuthContext";
import styles from "./ViewMembers.module.css";
import cx from "classnames";
import WwcApi from "../../WwcApi";
import MessageBox from "../messagebox/MessageBox";

import { ERROR_VOLUNTEER_RESOURCES_DOCUMENT_NOT_LOADED, ERROR_VOLUNTEER_RESOURCES_NO_DOCUMENT_AVAILABLE  } from "../../Messages";
import ResourcesLinks from "./ResourcesLinks";

const VolunteerResources = (props) => {

  const errorTitle = 'Sorry!';
  const [errorOnLoading, setErrorOnLoading] = useState(false);
  const [errorNoDocument, setErrorNoDocument] = useState(false);
  const [volunteerResource, setVolunteerResource] = useState({
    edit_link: "",
    published_link: ""
  });
  const { userInfo } = useContext(AuthContext);
  const isDirector = userInfo.role === "DIRECTOR";

  const slug = "volunteer_resource";
  //for social media: "social_media_resource",

  useEffect(() => {
    getVolunteerResources();
  }, []);

  const getVolunteerResources = async () => {
    try {
      let volunteerResources = await WwcApi.getVolunteerResources(slug);
      setVolunteerResource(volunteerResources)
    } catch (error) {
      console.log(error);
      if (error.response.status === 404) {
        setErrorNoDocument(true);
      } else
        setErrorOnLoading(true);
    }
  };

  const updateResources = (editLink, publishedLink) => {
    WwcApi.updateVolunteerResources(slug, {
      edit_link: editLink,
      published_link: publishedLink
    });
  };

  return (
    <div id='volunteerResourcesPage'
      className={cx(styles["view-member-page"], "d-flex flex-column")}
    >
      <div className={styles["view-member-page-list-wrapper"]}>
        <div className={styles["page-label-wrapper"]}>
          {isDirector && (
            <ResourcesLinks editUrl={volunteerResource.edit_link} publishUrl={volunteerResource.published_link} onSave={updateResources}></ResourcesLinks>
          )}
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