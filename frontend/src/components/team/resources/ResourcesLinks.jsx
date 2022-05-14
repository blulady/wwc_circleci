import React, { useEffect, useState } from "react";

import styles from "./ResourcesLinks.module.css";
import cx from "classnames";

const ResourcesLinks = (props) => {
    const [ isEditing, setIsEditing ] = useState(false);
    const [ editSaveTxt, setEditSaveTxt ] = useState("Edit Links");
    const [ editLink, setEditLink ] = useState(props.editUrl);
    const [ publishLink, setPublishLink ] = useState(props.publishUrl);

    useEffect(() => {
        setEditLink(props.editUrl);
        setPublishLink(props.publishUrl);
    }, [props.editUrl, props.publishUrl]);


    const saveOrEdit = () => {
        if (isEditing && props.onSave) {
            props.onSave(editLink, publishLink);
        }
        setIsEditing(!isEditing);
    };

    useEffect(() => {
        setEditSaveTxt(isEditing ? "Save Links" : "Edit Links");
    }, [isEditing]);

    const openEditDocument = () => {
        if (editLink) {
            window.open(editLink, "_blank");
        }
    };

    const onChangeEditLinks = (event) => {
        setEditLink(event.target.value);
    };

    const onChangePublishLinks = (event) => {
        setPublishLink(event.target.value);
    };

    return (
    <div className="row">
        <div className="col-12 col-md-8">
            <div className={styles["input-container"]}>
                <div className={cx(styles["input-label"], "mb-2")}>Edit URL:</div>
                <input type="text" readOnly={!isEditing} className={cx({ "form-control-plaintext": !isEditing, "wwc-text-input": isEditing }, styles["input-text"])} value={editLink} onChange={onChangeEditLinks} data-testid="editLink" />
            </div>
            <div className={styles["input-container"]}>
                <div className={cx(styles["input-label"], "mb-2")}>Published Embedded URL:</div>
                <input type="text" readOnly={!isEditing} className={cx({ "form-control-plaintext": !isEditing, "wwc-text-input": isEditing }, styles["input-text"])} value={publishLink} onChange={onChangePublishLinks} data-testid="publishLink" />
            </div>
        </div>
        <div className="col-12 col-md-4">
            <div className="d-flex justify-content-around">
                <button onClick={saveOrEdit} className="wwc-action-button" data-testid="saveBtn">
                    <div className="d-flex">
                        <span className="icon edit-purple-icon mr-2"></span>
                        {editSaveTxt}
                    </div>
                </button>
                <button onClick={openEditDocument} className="wwc-action-button">
                    <div className="d-flex">
                        <span className="icon edit-purple-icon mr-2"></span>
                        Edit Document
                    </div>
                </button>
            </div>
        </div>
    </div>);
};

export default ResourcesLinks;