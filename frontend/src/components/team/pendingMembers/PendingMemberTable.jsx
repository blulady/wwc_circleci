import React from "react";
import { useEffect } from "react";
import { useState } from "react";

import WwcApi from "../../../WwcApi";
import styles from "./PendingMemberTable.module.css";

const PendingMemberTable = (props) => {
    const users = props.users;

    const tableRows = users.map((user, idx) => 
        <tr key={idx}>
            <td>{idx + 1}</td>
            <td>{user.email}</td>
            <td className="wwc-text-capitalize">{user.role_name.toLowerCase()}</td>
            <td className="wwc-text-capitalize">{user.status.toLowerCase()}</td>
            <td>
                <button className={styles["invite-button"]} type="button" data-bs-toggle="modal" data-bs-target={props.target} data-bs-user={user.email}>Resend Invite</button>
            </td>
            <td>
                <button className={styles["delete"] + " " + styles["icon"]}></button>
            </td>
        </tr>
    );

    return (
        <table className={styles["pending-members-table"]}>
            <thead>
                <tr>
                    <th></th>
                    <th>Email</th>
                    <th>Role</th>
                    <th>Status</th>
                    <th>Resend Invite</th>
                    <th>Actions</th>
                </tr>
            </thead>
            <tbody>
                {tableRows}
            </tbody>
        </table>
    );
}

export default PendingMemberTable;