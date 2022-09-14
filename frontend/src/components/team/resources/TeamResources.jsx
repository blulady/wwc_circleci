import React, { useState, useEffect, useContext } from "react";
import cx from "classnames";
import AuthContext from "../../../context/auth/AuthContext";
import WwcApi from "../../../WwcApi";
import MessageBox from "../../messagebox/MessageBox";
import {
  ERROR_TEAM_RESOURCES_DOCUMENT_NOT_LOADED,
  ERROR_TEAM_RESOURCES_NO_DOCUMENT_AVAILABLE,
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

  const instructions = `
    <h5 class="c26">Instructions to set up Resource Document</h5>
    <ul>
      <li>Please create a Google Doc to be used for this resourcse document.</li>
      <li>Modify Share to 'Anyone on the internet with this link view.'</li>
      <li>Publish to the web: File -> Publish to the web -> Check 'Automatically republish when changes are made' -> Publish.</li>
      <li>Enter url in Enter URL field.</li>
      <li>Enter publish url in Published Embedded URL field.</li>
    </ul>`;

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

  const addNewResources = async (editLink, publishedLink) => {
    try {
      await WwcApi.addNewResources({
        edit_link: editLink,
        published_link: publishedLink,
        slug: slug
      });
    } catch (error) {
      setErrorNoDocument(true);
      setErrorNoDocumentMessage("cannot add new document, resource does not exist");
    }
  }

  const updateResources = async (editLink, publishedLink) => {
    try {
      await WwcApi.updateTeamResources(slug, {
        edit_link: editLink,
        published_link: publishedLink,
      });
    } catch (error) {
      if (error.response.status === 404) {
        setErrorNoDocument(true);
        setErrorOnLoading(true);
      }
    }
  };

  const messageBoxContent = () => {
    if (errorOnLoading) {
      return (
        <div className={"d-flex justify-content-center"}>
          <MessageBox
            type="Error"
            title={errorTitle}
            message={ERROR_TEAM_RESOURCES_DOCUMENT_NOT_LOADED}
          ></MessageBox>
        </div>
      )
    }
    else if (errorNoDocument) {
      return (
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
      )
    }
    else if (instructionsOnLoading) {
      return (
        <div
          className={cx(
            styles["instructions-box"],
            "d-flex align-items-left justify-content-left flex-column"
          )}
          data-testid="message-box-info"
        >
          <div dangerouslySetInnerHTML={{ __html: instructions }}></div>
        </div>
      )
    }
    else {
      return (
        <iframe
          className={styles["resources-frame"]}
          src={teamResource.published_link}
          title="Team Resources"
        ></iframe>
      )
    }
  }

  return (
    <React.Fragment>
      <div>
        {isDirector && (
          <ResourcesLinks
            editUrl={teamResource.edit_link}
            publishUrl={teamResource.published_link}
            onSaveFirstDocument={addNewResources}
            onUpdateDocument={updateResources}
          ></ResourcesLinks>
        )}
      </div>
      {messageBoxContent()}
    </React.Fragment>
  );
};
export default TeamResources;
