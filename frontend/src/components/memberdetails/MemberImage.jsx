import React from 'react';
import styles from "./MemberImage.module.css";


const MemberImage = ({image}) => {
  return (
    <div className={styles["view-member-image-div"]}>
      <img
        alt="Profiles"
        src={image}
        className={styles["img-size"]}
      />
    </div>
  )
}

export default MemberImage
