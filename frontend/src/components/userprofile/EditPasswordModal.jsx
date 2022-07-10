import React, { useState } from "react";
import Password from "../layout/Password"
import cx from "classnames";
import classes from "./UserProfile.module.css";
import WwcApi from "../../WwcApi";


const EditPasswordModal = (props) => {
    const [password, setPassword] = useState("");

    const handleSetPassword = async (pwd) => {
        setPassword(pwd);
    };
      
    const handleSubmit = async (evt) => {
        evt.preventDefault();
        let result = {
            status: null,
            update: "password",
        };
        try {
            const data = {"password": password};
            const response = await WwcApi.editUserPassword(data);
            result.status = "success";
        } catch (error) {
          console.log(error);
          result.status = "error"
        }
        props.submit(result);
    };

    return (
        <div>
            <div className={classes["edit-instructions"]}>
                <header className="text-center">
                    <div className={classes["modal-title-font"]}>Edit Password</div>
                    <div className={classes["edit-instructions"]}>
                        <p>Click in any field to make changes</p>
                        <p className={classes['warning']} id='warning'>
                            *All fields are mandatory
                        </p>
                    </div>
                </header>
            </div>

            <form onSubmit={handleSubmit} data-testid='edit-pw-form'>
                <Password setPwd={handleSetPassword}/>
                <div className='text-center'>
                    <button
                        type='submit'
                        className={cx('btn', classes['btn'], classes['confirm-btn'])}
                        data-testid='edit-pw-submit-button'
                        disabled={
                            !password
                        }
                    >
                    Confirm Changes
                    </button>
                    <button
                        className={cx('btn', classes['btn'], classes['cancel-btn'])}
                        data-testid='edit-pw-cancel-button'
                        onClick={(e) => {e.preventDefault(); props.closeEditModal();}}
                    >
                    Cancel
                    </button>
                </div>
            </form>

        </div>
    );
};

export default EditPasswordModal;
