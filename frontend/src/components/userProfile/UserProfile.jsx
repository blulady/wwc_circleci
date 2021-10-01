import React, { useState, useEffect, useContext } from "react";
import ContainerWithNav from "../layout/ContainerWithNav";
import AuthContext from "../../context/auth/AuthContext";
import WwcApi from "../../WwcApi";

import ActiveIcon from "../../images/Icon_Artwork.png";
import PendingIcon from "../../images/Icon_Artwork_Gray.png";
import ProfileImage from "../../images/ProfileImage.png";
import classes from "./UserProfile.module.css";
import cx from "classnames";

import MessageBox from "../messagebox/MessageBox";
import { ERROR_REQUEST_MESSAGE } from "../../Messages";

export const UserProfile = () => {
  const [profileData, setProfileData] = useState({})
  const { userInfo } = useContext(AuthContext);

  const [errorOnLoading, setErrorOnLoading] = useState(false);

  const getMyMemberData = async () => {
    try {
    let myMembership = await WwcApi.getMember(userInfo.id);
    setProfileData(myMembership);
    } catch (e) {
      setErrorOnLoading(true);
    }
  };

  useEffect(() => {
    getMyMemberData()
  }, [])

  const formatDate = (dateStr) => {
    if (!dateStr) {
      return "";
    }
    let d = new Date(dateStr);
    const options = { year: "numeric", month: "long", day: "numeric" };
    return d.toLocaleDateString("en-US", options);
  };
  return (
    <ContainerWithNav>

      <div className={`${classes.container}`}>
        {errorOnLoading && (
          <div className={cx(classes["error-container"], "d-flex justify-content-center py-4")}>
            <MessageBox type="Error" title="Sorry!" message={ERROR_REQUEST_MESSAGE}></MessageBox>
          </div>
        )}
        <div className={`${classes.formDiv}`}>
          <div className='row justify-content-center viewmember-form-div-spacing'>
            <div className='row justify-content-center viewmember-form-div-spacing'>
              <div className='row justify-content-center viewmember-form-div-spacing'>
                <div className="view-member-details-div">
                  <div className="col view-member-image-div mr-5">
                    <img src={ProfileImage} className={`${classes.imgSize}`}
                      style={{ width: "auto", height: "auto", borderRadius: "50%" }} />
                  </div>
                  <div className="col-lg-10 view-member-fields-div">
                    <div className={`${classes.profileName}`}>
                      <p>{profileData.first_name + " " + profileData.last_name}</p>
                      <p className={`${classes.userEmail} text-primary`}>{userInfo.email}</p>
                    </div>
                    <section className='section-box'>
                      <div className="datejoined-font block">
                        {"Member Since " + formatDate(profileData.date_joined)}
                      </div>
                      <div className={`${classes.status} mt-3 mb-3`}>
                        <span className="font-weight-bold pr-2">Status: </span>
                        <img
                          src={
                            profileData.status === "ACTIVE"
                              ? ActiveIcon
                              : PendingIcon
                          }
                          className={`${classes.statusIcon} pr-2`}

                          alt='Status'
                        /> {profileData.status}

                      </div>
                      <div className={`${classes.profileBorder} div-inline border-bottom mb-3`} />
                      <div className="role mb-3">
                        <span className="font-weight-bold"> Role:</span> {profileData.role}
                      </div>
                      <div className="role">
                        <span className="font-weight-bold"> Team:</span> {((profileData.teams || [{}])[0]).name}
                      </div>
                    </section>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </ContainerWithNav>
  )
}

export default UserProfile