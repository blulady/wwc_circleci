import React from 'react';
import styles from "./MemberImage.module.css";


const MemberImage = ({image}) => {
  return (
      <img
        alt="Profiles"
        src={image}
        className={styles["img-size"]}
      />
  )
}

export default MemberImage
