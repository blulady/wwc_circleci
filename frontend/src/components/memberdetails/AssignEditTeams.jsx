import React, {useState, useCallback} from 'react';
import styles from "./MemberDetails.module.css";
import classes from "./AssignEditTeams.module.css";
import cx from 'classnames';

const AssignEditTeams = ({role, selectedTeamsForThisRole = [], selectedTeamsForUser, totalTeams, editRoleTeams, setTeamEditMode}) => {

  const allSelectedTeams = new Set(selectedTeamsForUser);
  const [ selectedTeams, setSelectedTeams] = useState( new Set(selectedTeamsForThisRole));

  let getCheckboxClassName = (item) => {
    if (allSelectedTeams.has(item.name) && !selectedTeams.has(item.name)){
      return "disabled";
    }
    return selectedTeams.has(item.name) ? "checked" : "unchecked"
  };

   const handleSubmit = async(e) => {
    e.preventDefault();
    editRoleTeams(selectedTeams);
  }

  const handleClose = () => {
    setTeamEditMode(null);
  }

  const handleTeamChange = useCallback(
    (event) => {
      const { checked, value } = event.target;
      if (checked) {
        selectedTeams.add(value);
      } else {
        selectedTeams.delete(value);
      }
      setSelectedTeams(new Set(selectedTeams));
    },
    [selectedTeams]
  );

  return (
    <>
      <section data-testid="edit-teams"
        className={cx(styles["edit-member-form"])}
      >
        <form className={styles["form-container"]}>
          <div>
            <p className={classes["team-title"]}>Assign Team(s)</p>
            { role && totalTeams.map((item) => (
              <div className={classes["checkbox-container"]} key={item.id}>
                <label
                  className={cx(classes["custom-checkbox"], classes[getCheckboxClassName(item)])}
                >
                  <input
                    type="checkbox"
                    value={item.name}
                    onChange={handleTeamChange}
                    name="team"
                    checked={selectedTeams.has(item.name) ? "checked" : ""}
                    disabled = {!selectedTeams.has(item.name) && allSelectedTeams.has(item.name)}
                  />
                  <div className={cx("checkbox-icon", classes["checkbox-icon"])}></div>
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
            data-button="close"
            onClick={handleClose}
          >
            Cancel
          </button>
          <button 
            className={cx(styles["form-btn"], styles["btn-submit"], (!role) && styles['disabled'] )} 
            type="submit"
            onClick={role && handleSubmit}
          >
            Submit
          </button>
        </div>
      </section>
    </>
  )
}

export default AssignEditTeams;
