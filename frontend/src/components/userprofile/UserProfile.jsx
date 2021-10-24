import React, { useState, useEffect, useContext } from "react";
import ContainerWithNav from "../layout/ContainerWithNav";
import MemberImage from "../memberdetails/MemberImage";
import MemberInfoUnEditable from "../memberdetails/MemberInfoUnEditable";
import MemberStatus from "../memberdetails/MemberStatus";
import MemberRole from "../memberdetails/MemberRole";
import MemberTeams from "../memberdetails/MemberTeams";
import Spinner from "../layout/Spinner";
import ProfileImage from "../../images/ProfileImage.png";

import AuthContext from "../../context/auth/AuthContext";
import WwcApi from "../../WwcApi";

import styles from "../memberdetails/MemberDetails.module.css";
import cx from "classnames";

import MessageBox from "../messagebox/MessageBox";
import { ERROR_REQUEST_MESSAGE } from "../../Messages";

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
  const { userInfo } = useContext(AuthContext);

  const [errorOnLoading, setErrorOnLoading] = useState(false);

  useEffect(() => {
    const getMyMemberData = async () => {
      try {
      let myMembership = await WwcApi.getMember(userInfo.id);
      //TODO fix based on str returned once BE endpoint is ready
      let currentTeams = myMembership.teams.map(t=>t.name);
      myMembership['role_teams'] = {[myMembership.role]: currentTeams};
      setProfileData(myMembership);
      } catch (e) {
        setErrorOnLoading(true);
      }
    };
    getMyMemberData()
  }, [userInfo.id])

  const {date_joined, email, first_name, last_name,status, role_teams} = profileData;
  const roles = Object.keys(role_teams);
  return (
    <ContainerWithNav>
      <div className={styles["view-member-wrapper"]}>
        <div className={styles["member-container"]}>
          <div className={cx(styles["member-details-container"])} >
            {(errorOnLoading) && (
                <MessageBox type="Error" title="Sorry!" message={ERROR_REQUEST_MESSAGE}></MessageBox>
            )}
            {!profileData.first_name ? (
              <Spinner />
            ) : (
              <div className={cx("col-10", styles["view-member-fields-div"])}>
                <MemberImage image={ProfileImage} />
                <MemberInfoUnEditable first_name={first_name} last_name={last_name} email={email} date_joined={date_joined}/>
                <div className={styles["view-member-info-editable"]}>
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
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </ContainerWithNav>
  )
}

export default UserProfile