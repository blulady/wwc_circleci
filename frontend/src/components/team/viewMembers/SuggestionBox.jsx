import React from "react";

import styles from "./SuggestionBox.module.css";
import "../../../Common.css";
import cx from "classnames";

const SuggestionBox = (props) => {
    const onSelectOption = (ev) => {
        if (props.onSelect) {
            const target = ev.target;
            if(target.tagName.toLowerCase() === "li") {
                props.onSelect(target.textContent);
            }
        }
    };

    return (
        <div className={cx(styles["suggestion-box"], { hidden: !props.options.length })}>
            <ul onMouseDown={onSelectOption}>
                {props.options.map((option) => {
                    return <li value={option.id} key={option.id}>{option.value}</li>;
                })}
            </ul>
        </div>
    );
};

export default SuggestionBox;