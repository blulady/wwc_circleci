import React from "react";

import styles from "./MessageBox.module.css";
import cx from "classnames";

const MessageBox = (props) => {
    const type = {
        Info: "Info",
        Success: "Success",
        Error: "Error"
    };

    const getTypeStr = (str) => {
       return type[str] || this.type.Info;
    };

    return (<div className={cx(styles[getTypeStr(props.type).toLowerCase()], styles["message-box"], "d-flex align-items-center justify-content-center flex-column")}>
        <div className={styles["title"]}>{props.title}</div>
        <div className={styles["message"]}>
        {props.message}
        </div>
    </div>);
};
export default MessageBox;