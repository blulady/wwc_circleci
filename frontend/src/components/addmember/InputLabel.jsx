import React from "react";

const InputLabel = (props) => {
  return (
    <div>
      <label htmlFor={props.labelname} className="input-label">
        {props.text}
      </label>
    </div>
  );
};
export default InputLabel;
