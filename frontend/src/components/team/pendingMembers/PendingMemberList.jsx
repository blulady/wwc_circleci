import React from "react";
import { useEffect } from "react";
import { useState } from "react";
import WwcApi from "../../../WwcApi";
import styles from "./PendingMemberList.module.css";

const PendingMemberList = (props) => {
    const users = props.users;

    return (
        users.map((user, idx) =>
            <div className={styles["pending-member-list-card"] + " d-flex flex-column"} key={idx}>
                <div className={"align-self-end " + styles["icon"] + " " + styles["more"]}></div>
                <div className={"d-flex " + styles["row"]}>
                    <div className={styles["column"]}>Email</div>
                    <div className={styles["column"]}>{user.email}</div>
                </div>
                <div className={"d-flex " + styles["row"]}>
                    <div className={styles["column"]}>Role</div>
                    <div className={styles["column"]}>{user.role}</div>
                </div>
                <div className={"d-flex " + styles["row"]}>
                    <div className={styles["column"]}>Status</div>
                    <div className={styles["column"]}>{user.status}</div>
                </div>
                <div className={"d-flex " + styles["row"]}>
                    <div className={styles["column"]}>Resend Invite</div>
                    <div className={styles["column"]}><button className={styles["invite-button"] + " " + styles["icon"]}>Resend Invite</button></div>
                </div>
            </div>
        )
    );
}

export default PendingMemberList;