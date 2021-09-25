import React from "react";
import { useHistory } from "react-router-dom";
import ContainerWithNav from "../layout/ContainerWithNav";
import styles from "./Home.module.css";

/*
 * Home page - contains header and Chapter Members link in the body
 */

const Home = () => {
  const history = useHistory();

  const handleClick = (e) => {
    history.push("/members/chaptermembers");
  };

  return (
    <ContainerWithNav>
      <div className={styles.chaptermembers} onClick={handleClick}>
        <div className={styles.cardimgtop}></div>
        <div className={`${styles.cardbody} d-flex justify-content-center align-items-center`}>
          Chapter Members
        </div>
      </div>
    </ContainerWithNav>
  );
};

export default Home;
