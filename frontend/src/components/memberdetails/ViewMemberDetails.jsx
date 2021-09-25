import React, { useState, useEffect, useCallback } from "react";
import { useLocation, useHistory } from "react-router-dom";
import ContainerWithNav from "../layout/ContainerWithNav";
import EditIcon from "../../images/edit_24px.png";
import ActiveIcon from "../../images/Icon_Artwork.png";
import PendingIcon from "../../images/Icon_Artwork_Gray.png";
import BackButton from "../../images/arrow_back_24px.png";
import ProfileImage from "../../images/ProfileImage.png";
import RoleRadioInput from "../addmember/RoleRadioField";
import WwcApi from "../../WwcApi";
import styles from "./MemberDetails.module.css";
import cx from "classnames";

function ViewMemberDetails() {
  const history = useHistory();
  const location = useLocation();
  const data = location.state;
  const [user, setUser] = useState({});
  const [status, setStatus] = useState({ Status: "" });
  const [role, setRole] = useState({ Role: "" });
  const [editMode, setEditMode] = useState({ EditMode: false });
  const [teamEditMode, setTeamEditMode] = useState(false);
  const [teamsArray, setTeamsArray] = useState([]);
  const [teams, setTeams] = useState(new Set());

  const handleEditMode = () => {
    setEditMode({ EditMode: true });
  };

  const handleTeamEdit = () => {
    setTeamEditMode(true);
  };

  const MemberRoleArray = [
    {
      id: "1",
      role: "Volunteer",
      desc: "Limited access to areas of portal",
      value: "VOLUNTEER",
    },
    {
      id: "2",
      role: "Leader",
      desc: "Access to all areas excluding Director area",
      value: "LEADER",
    },
    {
      id: "3",
      role: "Director",
      desc: "Access to all areas of portal",
      value: "DIRECTOR",
    },
  ];

  const getMemberData = async (userid) => {
    try {
      let user = await WwcApi.getMember(userid);
      setUser(user);
      setRole({ Role: user.role });
      setStatus({ Status: user.status });
      setTeams(new Set(user.teams));
    } catch (error) {
      console.log(error);
    }
  };
  const getTeamsData = async () => {
    try {
      let data = await WwcApi.getTeams();
      setTeamsArray(data);
    } catch (error) {
      console.log(error);
    }
  };

  useEffect(() => {
    getMemberData(data.id);
    getTeamsData();
  }, [data]);

  const formatDate = (dateStr) => {
    if (!dateStr) {
      return "";
    }
    let d = new Date(dateStr);
    const options = { year: "numeric", month: "long", day: "numeric" };
    return d.toLocaleDateString("en-US", options);
  };

  const handleRoleChange = (id) => {
    MemberRoleArray.forEach((item) => {
      if (item.id === id) {
        setRole({ Role: item.value });
      }
    });
  };

  const handleChange = (event) => {
    setStatus({ Status: event.target.value });
  };

  const handleTeamChange = useCallback(
    (event) => {
      const { checked, value } = event.target;
      if (checked) {
        teams.add(value);
      } else {
        teams.delete(value);
      }
      setTeams(new Set(teams));
    },
    [teams]
  );

  const onClickSubmit = async (event) => {
    let userId = user.id;
    alert("submtting data");
    event.preventDefault();
    const memberInfo = {
      role: role.Role,
      status: status.Status,
    };
    try {
      WwcApi.editMember(memberInfo, userId);
      history.push({
        pathname: "/viewMembers",
      })} catch (error) {
        console.log(error);
      }
  };

  let editRoleClassName = editMode.EditMode && user.status !== "PENDING" ? styles["show-form"] : styles["hide-form"] + " responsive-role-div";
  let editTeamClassName = teamEditMode && user.status !== "PENDING" ? styles["show-form"] : styles["hide-form"];
  let getCheckboxClassName = (item) => {return teams.has(item.name) ? styles["checked"] : styles["unchecked"]};

  return (
    <ContainerWithNav>
      <main>
        <div className="container">
          <div className="button-inside-div">
            <button
              className="chapter-member-btn"
              onClick={() => {
                history.push({ pathname: "/home" });
              }}
            >
              Chapter Members
            </button>
          </div>
          <div className={styles["member-container"]}>
            <div className="back-member-img-btn-div">
              <img
                src={BackButton}
                className="back-btn-img"
                style={{ width: "auto", height: "auto" }}
                alt="Back Button"
              />
              <button
                className="back-member-btn"
                onClick={() => {
                  history.push({ pathname: "/viewMembers" });
                }}
              >
                Back to Member Portal
              </button>
            </div>

            <div
              className={cx(styles["member-details-container"], { "bottom-spacing": editMode.EditMode || teamEditMode })}
            >
              <div className="row justify-content-center">
                <div className={cx("row", "justify-content-end", styles["view-member-details-div"])}>
                  <div className={cx("col-lg-3", "col-2", styles["view-member-image-div"])}>
                    <img
                      alt="Profiles"
                      src={ProfileImage}
                      className="img-size"
                    />
                  </div>
                  <div className={cx("col-lg-9", "col-10", styles["view-member-fields-div"])}>
                    <div className={styles["fullname-font"]}>
                      {user.first_name + " " + user.last_name}
                    </div>
                    <div className={styles["email-font"]}>{user.email}</div>
                    <div className={styles["datejoined-font"]}>
                      {"Member Since " + formatDate(user.date_joined)}
                    </div>
                  </div>
                  <div className={cx("col-lg-9", "col-md-10", "col-12", styles["view-member-fields-edit-div"])}>
                    <section className={styles["section-box"]}>
                      <div className={styles["col-wrapper"]}>
                        <div className={styles["label-font"]}>Status:</div>
                        <div className={styles["status-icon-wrapper"]}>
                          <img
                            src={
                              user.status === "ACTIVE"
                                ? ActiveIcon
                                : PendingIcon
                            }
                            className={styles["status-icon"]}
                            alt="Status"
                          />
                        </div>

                        <div className={styles["member-info-text"]}>
                          {status.Status.toLowerCase()}
                        </div>
                      </div>
                      {editMode.EditMode ||
                      teamEditMode ||
                      user.status === "PENDING" ? (
                        ""
                      ) : (
                        <div className="edit-icon-wrapper">
                          <img
                            src={EditIcon}
                            className={styles["edit-icon"]}
                            alt="Edit-status"
                            onClick={handleEditMode}
                          />
                        </div>
                      )}
                    </section>
                    <section className={styles["section-box"]}>
                      <div className={styles["col-wrapper"]}>
                        <div className={styles["label-font"]}>Role:</div>
                        <div className={styles["member-info-text"]}>
                          {role.Role?.toLowerCase()}
                        </div>
                      </div>
                      <div className="edit-icon-wrapper">
                        {editMode.EditMode ||
                        teamEditMode ||
                        user.status === "PENDING" ? (
                          ""
                        ) : (
                          <img
                            className={styles["edit-icon"]}
                            src={EditIcon}
                            alt="Edit-role"
                            onClick={handleEditMode}
                          />
                        )}
                      </div>
                    </section>
                    <section className={styles["section-box"]}>
                      <div className={styles["col-wrapper"]}>
                        <div className={styles["label-font"]}>
                          Team
                          {[...teams].length > 0 && (
                            <span className={styles["label-font"]}>:</span>
                          )}
                        </div>
                        <div className={styles["member-info-text"]} data-testid="teams">
                          {[...teams].join(",")}
                        </div>
                      </div>
                      <div className="edit-icon-wrapper">
                        {editMode.EditMode ||
                        teamEditMode ||
                        user.status === "PENDING" ? (
                          ""
                        ) : (
                          <img
                            className={styles["edit-icon"]}
                            src={EditIcon}
                            alt="Edit-team"
                            onClick={handleTeamEdit}
                          />
                        )}
                      </div>
                    </section>
                  </div>
                </div>
              </div>
            </div>
            <section data-testid="edit-role-status"
              className={cx(styles["edit-member-form"], editRoleClassName)}
            >
              <form>
                <section>
                  <label labelname="role" className={styles["edit-section-label-font"]}>
                    Role
                  </label>
                  <br />
                  <div className="div-inline responsive-div-block">
                    <div>
                      {MemberRoleArray.map((item) => (
                        <div
                          key={item.id}
                          className={cx({"radio-btn-selected" : item.value === role.Role}, {"radio-input": item.value !== role.Role})}
                        >
                          <RoleRadioInput
                            checked={item.value === role.Role}
                            id={item.id}
                            name="Role"
                            value={item.value}
                            pclass={editMode.EditMode ? "show" : "hide"}
                            datatarget="#confirmModal"
                            onChange={() => handleRoleChange(item.id)}
                            roletext={item.role}
                            roledesc={item.desc}
                          />
                        </div>
                      ))}
                    </div>
                  </div>
                </section>
                <br />

                <section>
                  <div className={styles["edit-separator"]}></div>
                  <label labelname="status" className={styles["edit-section-label-font"]}>
                    Status
                  </label>
                  <span
                    className={cx({"radio-btn-selected": status.Status === "ACTIVE"}, { "radio-input": status.Status !== "ACTIVE"})}
                  >
                    <input
                      checked={status.Status === "ACTIVE"}
                      type="radio"
                      id="active"
                      name="Status"
                      value="ACTIVE"
                      onChange={handleChange}
                    />
                    <label className={styles["member-role"]} htmlFor="active">
                      Active
                    </label>
                    <br />
                  </span>

                  <span className={cx({"radio-btn-selected": status.Status === "INACTIVE"}, { "radio-input": status.Status !== "INACTIVE"})}>
                    <input
                      checked={status.Status === "INACTIVE"}
                      type="radio"
                      id="inactive"
                      name="Status"
                      value="INACTIVE"
                      onChange={handleChange}
                    />
                    <label className={styles["member-role"]} htmlFor="Inactive">
                      Inactive
                    </label>
                  </span>
                </section>
                <div className="form-group d-flex justify-content-center">
                  <input
                    type="button"
                    className={cx(styles["form-btn"], styles["btn-submit"])}
                    onClick={onClickSubmit}
                    value="Submit"
                  />
                </div>
              </form>
            </section>
            <section data-testid="edit-teams"
              className={cx("edit-member-form", editTeamClassName)}
            >
              <form className={styles["form-container"]}>
                <div>
                  <p className={styles["team-title"]}>Team</p>
                  {teamsArray.map((item) => (
                    <div className={styles["checkbox-container"]} key={item.id}>
                      <label
                        className={cx(styles["custom-checkbox"], getCheckboxClassName(item))}
                      >
                        <input
                          type="checkbox"
                          value={item.name}
                          onChange={handleTeamChange}
                          name="team"
                        />
                        <div className={cx("checkbox-icon", styles["checkbox-icon"])}></div>
                        {item.name}
                      </label>
                    </div>
                  ))}
                </div>
              </form>
              <div className={styles["form-buttons-container"]}>
                <button
                  className={cx(styles["form-btn"], styles["btn-cancel"])}
                  type="button"
                  onClick={() => setTeamEditMode(false)}
                >
                  Cancel
                </button>
                <button className={cx(styles["form-btn"], styles["btn-submit"])} type="submit">
                  Submit
                </button>
              </div>
            </section>
          </div>
        </div>
      </main>
    </ContainerWithNav>
  );
}
export default ViewMemberDetails;
