import React from "react";
import { useEffect } from "react";
import { useState } from "react";
import { isBrowser } from "react-device-detect";
import { useNavigate } from "react-router-dom";
import WwcApi from "../../../WwcApi";
import PendingMemberList from "./PendingMemberList";
import PendingMemberTable from "./PendingMemberTable";
import styles from "./PendingMembers.module.css";
import MessageBox from "../../messagebox/MessageBox";
import { ERROR_TEAM_MEMBERS_UNABLE_TO_LOAD } from "../../../Messages";

const PendingMembers = (props) => {
    const [users, setUsers] = useState([]);
    const [errorOnLoading, setErrorOnLoading] = useState(false);
    const navigate = useNavigate();
    const renderTable = () => {
        return <PendingMemberTable users={users}></PendingMemberTable>;
    };
    const renderList = () => {
        return <PendingMemberList users={users}></PendingMemberList>;
    };

    const getInvitees = async () => {
        try {
            let _users = await WwcApi.getInvitees();
            setUsers(_users);
        } catch (error) {
            setErrorOnLoading(true);
            console.log(error);
        }
    };

    const goToAddMember = () => {
        navigate("/member/add");
    };

    useEffect(() => {
        getInvitees();
    }, []);

    if (errorOnLoading) {
        return (
            <div className={styles["error-container"] + " d-flex justify-content-center"}>
                <MessageBox
                    type="Error"
                    title="Sorry!"
                    message={ERROR_TEAM_MEMBERS_UNABLE_TO_LOAD.replace("{0}", "")}
                ></MessageBox>
            </div>)
    } else {
        return (
            <div>
                <div className="d-flex justify-content-end mb-2 mb-md-5">
                    <button type="button" className="wwc-action-button" onClick={goToAddMember}>+ Add Member</button>
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
}

export default PendingMembers;