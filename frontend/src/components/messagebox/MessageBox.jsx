import React from "react";

import styles from "./MessageBox.module.css";
import cx from "classnames";

const MessageBox = (props) => {
  const type = {
    Info: "Info",
    Success: "Success",
    Error: "Error",
    Instructions: "Instructions",
  };

  const contentType = props.contentType;

  const getTypeStr = (str) => {
    return type[str] || this.type.Info;
  };

  return (
    <div>
      {props.type === "Instructions" ? (
        <div
          className={cx(
            styles[getTypeStr(props.type).toLowerCase()],
            styles["message-box-instructions"],
            "d-flex align-items-center justify-content-center flex-column"
          )}
          data-testid="message-box-info"
        >
          <div className={styles["title"]}>{props.title}</div>
          {contentType == "html" ? (
            <div
              className={styles["message"]}
              dangerouslySetInnerHTML={{ __html: props.message }}
            ></div>
          ) : (
            <div className={styles["message"]}>{props.message}</div>
          )}
        </div>
      ) : (
        <div
          className={cx(
            styles[getTypeStr(props.type).toLowerCase()],
            styles["message-box"],
            "d-flex align-items-center justify-content-center flex-column"
          )}
          data-testid="message-box"
        >
          <div className={styles["title"]}>{props.title}</div>
          {contentType == "html" ? (
            <div
              className={styles["message"]}
              dangerouslySetInnerHTML={{ __html: props.message }}
            ></div>
          ) : (
            <div className={styles["message"]}>{props.message}</div>
          )}
        </div>
      )}
    </div>
  );
};
export default MessageBox;
