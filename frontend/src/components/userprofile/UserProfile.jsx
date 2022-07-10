import React, { useState, useEffect } from "react";
import ContainerWithNav from "../layout/ContainerWithNav";
import MemberImage from "../memberdetails/MemberImage";
import UserInfoUnEditable from "./UserInfoUnEditable";
import MemberStatus from "../memberdetails/MemberStatus";
import MemberRole from "../memberdetails/MemberRole";
import MemberTeams from "../memberdetails/MemberTeams";
import Spinner from "../layout/Spinner";
import ProfileImage from "../../images/ProfileImage.png";

import AuthContext from "../../context/auth/AuthContext";
import WwcApi from "../../WwcApi";

import styles from "../memberdetails/MemberDetails.module.css";
import classes from "./UserProfile.module.css"
import cx from "classnames";

import MessageBox from "../messagebox/MessageBox";
import { ERROR_REQUEST_MESSAGE, SUCCESS_USER_PROFILE } from "../../Messages";

import UserName from "./UserName";
import EditNameModal from "./EditNameModal";
import EditPasswordModal from "./EditPasswordModal";

export const UserProfile = () => {

  const [profileData, setProfileData] = useState({
    date_joined: "",
    email: "",
    first_name: "",
    id: null,
    last_name: "",
    status: "",
    role_teams: {
      // 'DIRECTOR':[],
      // 'LEADER': ["Event Volunteers","Volunteer Management"],
      // 'VOLUNTEER': ["Partnership Management","Social Media","Host Management"]
    }
  })

  const {date_joined, email, first_name, last_name,status, role_teams} = profileData;
  const roles = Object.keys(role_teams);

  const [showEditModal, setShowEditModal] = useState({modal: null});
  const [message, setMessage] = useState({show: false});

  useEffect(() => {
    const getMyMemberData = async () => {
      try {
      let myMembership = await WwcApi.getUserProfile();
      let role_teams = {};
      myMembership.role_teams.forEach((t) => {
        // {
        //   "team_id": 5,
        //   "team_name": "Social Media",
        //   "role_name": "DIRECTOR"
        // },
        (t.role_name in role_teams) || (role_teams[t.role_name] = []);
        if (t.team_name) {
          role_teams[t.role_name].push(t.team_name);
        }
      });
      myMembership['role_teams'] = role_teams;
      setProfileData(myMembership);
      } catch (e) {
        setMessage({
          show: true,
          type:"Error",
          title: "Sorry!",
          content: ERROR_REQUEST_MESSAGE
        });

      }
    };
    getMyMemberData()
  }, [])

  const showModal = (modal) => {
    setShowEditModal({modal});
    setMessage({show: false}); // Clear any messages
  }

  const closeModals = () => {
    setShowEditModal({modal: null});
  }

  const handleChangePasswordButton = () => {
    showModal("password");
  };

  const handleNameEditIcon = () => { // Launch name edit modal
    showModal("name");
  };

  const handleCancelEdit = () => { 
    closeModals();
    setMessage({show: false}); // Clear any messages
  };

  const handleProfileChange = async (result) => {
    if (result.status === "success") {
      if (result.update === "name") {
        setProfileData({...profileData, first_name: result.nameInfo.first_name, last_name: result.nameInfo.last_name});
      }
        setMessage({ // Show success message
          show: true,
          type:"Success",
          title: "Success!",
          content: SUCCESS_USER_PROFILE
        });
        closeModals();
    } else {
      setMessage({ // Show error message and keep modal open
        show: true,
        type:"Error",
        title: "Sorry!",
        content: ERROR_REQUEST_MESSAGE
      });
    }
  };


  return (
    <ContainerWithNav>
      <div className={styles["view-member-wrapper"]}>
        <div className={styles["member-container"]}>
          <div className={styles["member-details-container"]} >
            {(message.show) && (
                <MessageBox type={message.type} title={message.title} message={message.content}></MessageBox>
            )}
            {!profileData.first_name ? (
              <div className="text-center">
                <Spinner />
              </div>
            ) : (
              <>
              {(showEditModal.modal === null && 
              <button
                className={cx('btn', classes['btn'], classes['change-pw-btn'])}
                data-testid='change-password-button'
                onClick={handleChangePasswordButton}
              >Change Password</button>
              )}
              <div className={cx("col-10", styles["view-member-fields-div"])}>
                <div className="row">
                  <div className="col-12 col-lg-4"> {/* image column */}
                    <div className={classes["view-user-image-div"]}>
                      <MemberImage image={ProfileImage} />
                    </div> 
                  </div> {/* image column end */}
                  <div className="col-12 col-lg-8"> {/* info column */}
                  {(showEditModal.modal === "name"  &&
                    <EditNameModal
                    firstName={first_name}
                    lastName={last_name}
                    submit={handleProfileChange}
                    closeEditModal={handleCancelEdit}
                    />
                    )}
                    {(showEditModal.modal === "password" && 
                    <EditPasswordModal
                    submit={handleProfileChange}
                    closeEditModal={handleCancelEdit}
                    />
                    )}
                    { (showEditModal.modal === null &&
                    <div> {/* start edit modal occlusion */}
                      <div className={classes["view-user-name-email-date"]}>
                        <UserName
                          firstName={first_name}
                          lastName={last_name}
                          showEditModal={handleNameEditIcon}
                        />
                        <UserInfoUnEditable
                          email={email}
                          date_joined={date_joined}
                        />
                      </div> {/* end view-user-name-email-date*/}
          
                      <div>
                        <MemberStatus status={status}/>
                        {roles.map(
                          (role) => (
                            <section key={role}>
                              <MemberRole role={role} status={status} numRoles={roles.length}/>
                              <MemberTeams role={role} teams={role_teams[role]} status={status}/>
                              <hr className={styles["section-divider" ]}/>
                            </section>
                          )
                        )}
                      </div> {/* end view-member-info-editable */}

                    </div> //* end edit modal occlusion
                    )}
                  </div> {/* info column end */}
                </div> {/* row end */}
              </div> {/* end "view-member-fields-div" */}
            </> // end loaded content
            )} 
          </div> {/* end "member-details-container" */}
        </div> {/* end "member-container" */}
      </div> {/* end "view-member-wrapper" */}
    </ContainerWithNav>
  )
}

export default UserProfile