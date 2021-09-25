import React, { useState } from "react";

import styles from "./SearchBox.module.css";
import cx from "classnames";

const SearchBox = (props) => {

    //const [filterBoxState, setFilterBoxState] = useState(false);

    const onSearchChange = (ev) => {
        if(props.onSearchChange) {
            props.onSearchChange(ev.target.value);
        }
    };

    const onBlur = (ev) => {
        if(props.onBlur) {
            props.onBlur();
        }
    };

    const onFocus = () => {
        if(props.onFocus) {
            props.onFocus();
        }
    };

/*     const toggleFilterBox = () => {
        setFilterBoxState(!filterBoxState);
    }; */

    const onEnter = (ev) => {
        if (ev.keyCode === 13) {
            if(props.onEnter) {
                props.onEnter(ev.target.value);
            }
        }
    }

    return (
        <div className={cx(styles["search-box"] ,"input-group")}>
            <div className={styles["search-box-prepend"] + " input-group-prepend"}>
                <div className="input-group-text bg-transparent"><i className="fa fa-search"></i></div>
            </div>
            <input type="text" className={cx(styles["search-text"], "form-control border-left-0")} placeholder="Search For Name" aria-label="Search Box" onChange={onSearchChange} onBlur={onBlur} onFocus={onFocus} onKeyUp={onEnter}></input>
        </div>
    );
};

export default SearchBox;