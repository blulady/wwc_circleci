import React from 'react';

import styles from "./WwcBackground.module.css";

function WwcBackground(props) {

  return (
    <div className={styles["WwcBackground"]}>
      <div className={styles["WwcBackground-opacity"]}>
        {props.children}
      </div>
    </div>
  );
}

export default WwcBackground;