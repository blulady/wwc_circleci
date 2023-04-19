import React from "react";
import styles from "./PendingMemberList.module.css";
import "../../../Common.css";

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
                    <div className={styles["column"] + " wwc-text-capitalize"}>{user.role_name.toLowerCase()}</div>
                </div>
                <div className={"d-flex " + styles["row"]}>
                    <div className={styles["column"]}>Status</div>
                    <div className={styles["column"] + " wwc-text-capitalize"}>{user.status.toLowerCase()}</div>
                </div>
                <div className={"d-flex " + styles["row"]}>
                    <div className={styles["column"]}>Resend Invite</div>
                    <div className={styles["column"]}><button className={styles["invite-button"] + " " + styles["icon"]} data-bs-toggle="modal" data-bs-target={props.target} data-bs-user={user.email}>Resend Invite</button></div>
                </div>
            </div>
        )
    );
}

export default PendingMemberList;