import React from "react";

const RoleRadioInput = (props) => {
  return (
    <>
      <input
        checked={props.checked}
        type="radio"
        className={props.className}
        id={props.id}
        name={props.name}
        value={props.value}
        data-toggle="modal"
        data-target={props.datatarget}
        onClick={props.onClick}
        onChange={props.onChange}
      />
      <div className="member-role">{props.roletext}</div>
      <div className="role-desc">{props.roledesc}</div>
    </>
  );
};
export default RoleRadioInput;
