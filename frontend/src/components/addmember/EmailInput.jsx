import React from "react";
import EditIcon from "../../images/edit_24px.png";

const EmailInput = (props) => {
  return (
    <div className="div-inline responsive-div-block">
      <p className={props.pclass}>{props.emailvalue}</p>
      <input
        type="email"
        className={props.className}
        id="email"
        name={props.name}
        value={props.value}
        onChange={props.onChange}
        placeholder={props.placeholder}
        required
      />
      <div className="spacer" />
      <div className="edit-icon">
        <img
          className={props.editclass}
          src={EditIcon}
          style={{ width: "auto", height: "auto" }}
          alt="Edit"
          onClick={props.editiconclick}
        />
      </div>
      {/* <button  className={props.buttonclass} onClick={props.savebuttonclick}> */}
      <button type="submit" className={props.buttonclass} onClick={props.savebuttonclick}>
        Save
      </button>
    </div>
  );
};
export default EmailInput;
