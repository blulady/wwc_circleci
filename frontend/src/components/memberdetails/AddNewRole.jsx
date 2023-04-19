import React, {useState} from 'react';
import ConfirmationModal from '../addmember/ConfirmationModal';

import styles from "./MemberDetails.module.css";
import classes from "./AddNewRole.module.css";
import cx from "classnames";

const AddNewRole = ({selectedRolesForUser, allRoles, addNewRole}) => {

  const [role, setRole] = useState({id: null, role: '', value: '', desc: ''});
  const [selectedRoles] = useState(new Set(selectedRolesForUser));

  const handleRoleChange = (e, id) => {
    allRoles.forEach((item) => {
      if (item.id === id) {
        setRole({...item});
        addNewRole({...item});
      }
    });
  };

  return (
    <>
      <section className={styles["section-box"]}
      >
        <form className={classes['add-new-role']}>
          <div>
            <div labelname="role" className={styles["label-font"]}>
              Assign Role
            </div>
            <div className="mt-4">
                {allRoles.map((item) => (
                  <div
                    key={item.id}
                    className={cx(classes["role-radio-div"], role.role === item.role && classes['role-radio-div-selected'])}
                  >
                    <input
                      disabled = {selectedRoles.has(item.value)}
                      type="radio"
                      className={cx(classes["radio-btn"])}
                      id={item.id}
                      name="Role"
                      value={item.role}
                      data-bs-toggle="modal"
                      data-bs-target="#confirmModal"
                      onChange={(e) => handleRoleChange(e,item.id)}
                    />
                    <div className={cx(classes["custom-radio-btn"],selectedRoles.has(item.value) && classes['disabled'], role.role === item.role && classes['selected'] )}></div>
                    <label className={cx(classes["member-role"], selectedRoles.has(item.value) ? classes['disabled'] : classes['active'])}>{item.role}
                      <span className={classes["role-desc"]}>{item.desc}</span>
                    </label>
                  </div>
                ))}
                <ConfirmationModal
                  memberrole={role.value.toLowerCase()}
                  memberdesc={role.desc}
                />
            </div>
          </div>
          <br />
        </form>
        </section>
    </>
  )
}

export default AddNewRole;
