import React, { useState, useEffect, useContext } from "react";
import cx from "classnames";
import AuthContext from "../../../context/auth/AuthContext";
import WwcApi from "../../../WwcApi";
import MessageBox from "../../messagebox/MessageBox";

import {
  ERROR_TEAM_RESOURCES_DOCUMENT_NOT_LOADED,
  ERROR_TEAM_RESOURCES_NO_DOCUMENT_AVAILABLE,
  INSTRUCTIONS_MESSAGE,
} from "../../../Messages";
import ResourcesLinks from "./ResourcesLinks";
import { useParams } from "react-router-dom";
import { useTeamContext } from "../../../context/team/TeamContext";
import styles from "./TeamResources.module.css";

const TeamResources = (props) => {
  const errorTitle = "Sorry!";
  const [errorOnLoading, setErrorOnLoading] = useState(false);
  const [errorNoDocument, setErrorNoDocument] = useState(false);
  const [errorNoDocumentMessage, setErrorNoDocumentMessage] = useState("");
  const [instructionsOnLoading, setInstructionsOnLoading] = useState(false);
  const [teamResource, setTeamResource] = useState({
    edit_link: "",
    published_link: "",
  });
  const { userInfo } = useContext(AuthContext);
  const isDirector = userInfo.role === "DIRECTOR";

  const params = useParams();
  const team = params.team;

  const { teams } = useTeamContext();
  const teamInfo = teams[team];

  const slug = teamInfo.slug;

  useEffect(() => {
    getTeamResources();
  }, []);

  const getTeamResources = async () => {
    try {
      let teamrResources = await WwcApi.getTeamResources(slug);
      setTeamResource(teamrResources.data);
    } catch (error) {
      if (error.response.status === 404) {
        setInstructionsOnLoading(true);
      } else setErrorOnLoading(true);
    }
  };

  const updateResources = async (editLink, publishedLink, errorMessage) => {
    try {
      await WwcApi.updateTeamResources(slug, {
        edit_link: editLink,
        published_link: publishedLink,
      });
    } catch (error) {
      if (error.response.status === 404) {
        setErrorNoDocument(true);
        if (typeof errorMessage != "undefined") {
          setErrorNoDocumentMessage(errorMessage);
        }
      } else setErrorOnLoading(true);
    }
  };

  return (
    <React.Fragment>
      <div>
        {isDirector && (
          <ResourcesLinks
            editUrl={teamResource.edit_link}
            publishUrl={teamResource.published_link}
            onSave={updateResources}
          ></ResourcesLinks>
        )}
      </div>
      {errorOnLoading && (
        <div className={"d-flex justify-content-center"}>
          <MessageBox
            type="Error"
            title={errorTitle}
            message={ERROR_TEAM_RESOURCES_DOCUMENT_NOT_LOADED}
          ></MessageBox>
        </div>
      )}
      {errorNoDocument && (
        <div className={"d-flex justify-content-center"}>
          <MessageBox
            type="Error"
            title={errorTitle}
            message={
              errorNoDocumentMessage.length == 0
                ? ERROR_TEAM_RESOURCES_NO_DOCUMENT_AVAILABLE
                : errorNoDocumentMessage
            }
          ></MessageBox>
        </div>
      )}
      {instructionsOnLoading && (
        <div
          className={cx(
            styles["error-container"],
            "d-flex justify-content-left"
          )}
        >
          <MessageBox
            contentType="html"
            type="Instructions"
            message={INSTRUCTIONS_MESSAGE}
          ></MessageBox>
        </div>
      )}
      {!errorNoDocument && !errorOnLoading && !instructionsOnLoading && (
        <iframe
          className={styles["resources-frame"]}
          src={teamResource.published_link}
          title="Team Resources"
        ></iframe>
      )}
    </React.Fragment>
  );
};
export default TeamResources;
