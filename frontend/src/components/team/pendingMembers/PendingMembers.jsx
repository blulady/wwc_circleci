import React from "react";
import { useEffect } from "react";
import { useState } from "react";
import { isBrowser } from "react-device-detect";
import WwcApi from "../../../WwcApi";
import PendingMemberList from "./PendingMemberList";
import PendingMemberTable from "./PendingMemberTable";
import styles from "./PendingMembers.module.css";

const PendingMembers = (props) => {
    const [users, setUsers] = useState([]);
    const renderTable = () => {
        return <PendingMemberTable users={users}></PendingMemberTable>;
    };
    const renderList = () => {
        return <PendingMemberList users={users}></PendingMemberList>;
    };

    useEffect(() => {
        setUsers([
            {
                email: "abc@example.com",
                role: "Director",
                status: "Invited"
            },
            {
                email: "abc@example.com",
                role: "Director",
                status: "Invited"
            },
            {
                email: "abc@example.com",
                role: "Director",
                status: "Invited"
            },
            {
                email: "abc@example.com",
                role: "Director",
                status: "Invited"
            },
            {
                email: "abc@example.com",
                role: "Director",
                status: "Invited"
            }
        ]);
    }, []);

    return (
        <div>
            <div className="d-flex justify-content-end mb-2 mb-md-5">            
                <button type="button"className="wwc-action-button">+ Add Member</button>
            </div>
            {
                users.length ? (
                    isBrowser ? renderTable() : renderList()
                ) : (
                    <div className={styles["no-users-msg"]}>No invitees to display</div>
                )
            }
        </div>
    );
}

export default PendingMembers;