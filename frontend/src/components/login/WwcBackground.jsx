import React from 'react';

import "./WwcBackground.css";

function WwcBackground(props) {

  return (
    <div className="WwcBackground">
      <div className="WwcBackground-opacity">
        {props.children}
      </div>
    </div>
  );
}

export default WwcBackground;