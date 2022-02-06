import React from "react";
import EditIcon from "../../images/edit_24px.png";

const TextAreaInput = (props) => {
  return (
    <div className="div-inline responsive-div-block">
      <p className={props.memberclass}>{props.message}</p>
      <div style={{ display: "block" }}>
        <textarea
          className={props.className}
          id="message"
          name={props.name}
          value={props.value}
          rows="6"
          placeholder="Add an optional message to the registration email sent to the user (max 2000 char)"
          onChange={props.onChange}
          maxLength="2000"
          data-testid='message'
        ></textarea>
        <div className={props.counterclass}>{props.countervalue}</div>
      </div>
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
      <button type= "submit" className={props.buttonclass} onClick={props.savebuttonclick}>
        Save
      </button>
    </div>
  );
};
export default TextAreaInput;
