import React from "react";
import AssignEditTeams from "./AssignEditTeams";

import styles from "./MemberDetails.module.css";
import classes from "./MemberTeams.module.css";
import cx from "classnames";

const MemberTeams = ({
  role,
  teams,
  status,
  modifyTeams = null,
  totalTeams = null,
  allSelectedTeams = null,
  editing = null,
  setEditing = null,
}) => {
  const handleIconClick = (e) => {
    if (editing) return;
    setEditing(role);
  };

  const handleEditTeams = (selectedTeams) => {
    modifyTeams(role, selectedTeams);
  };
  return (
    <section className={styles["section-box"]}>
      {!editing || (editing && editing !== role) ? (
        <>
          <div
            className={styles["col-wrapper"]}
            style={{ alignItems: "flex-start" }}
          >
            <div className={styles["label-font"]}>Team:</div>
            <div
              className={cx(
                classes["team-info-text"],
                styles["member-info-text"]
              )}
              data-testid="teams"
            >
              <ul className={classes["team-info-list"]}>
                {teams.map((teamName) => (
                  <li key={teamName}>{teamName}</li>
                ))}
              </ul>
            </div>
          </div>
          <div
            id="team-edit"
            className={styles["icon-wrapper"]}
            onClick={status === "ACTIVE" ? handleIconClick : null}
          >
            {status === "PENDING" || !modifyTeams ? (
              ""
            ) : (
              <>
                <i
                  className={cx(
                    "fas fa-pen",
                    styles["member-info-icon"],
                    status === "ACTIVE" && !editing
                      ? styles["member-icon-active"]
                      : styles["member-icon-inactive"]
                  )}
                ></i>
                <p className={styles["change-status-text"]}>
                  {teams.length ? "Edit Teams" : "Assign Teams"}
                </p>
              </>
            )}
          </div>
        </>
      ) : (
        <AssignEditTeams
          role={role}
          selectedTeamsForThisRole={teams}
          selectedTeamsForUser={allSelectedTeams}
          totalTeams={totalTeams}
          editRoleTeams={handleEditTeams}
          status={status}
          setTeamEditMode={setEditing}
          assigning={!teams.length}
        />
      )}
    </section>
  );
};

export default MemberTeams;
