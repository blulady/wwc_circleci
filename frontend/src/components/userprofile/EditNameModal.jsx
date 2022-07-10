import React, { useState } from "react";
import cx from "classnames";
import classes from "./UserProfile.module.css";
import styles from "../register/Register.module.css";
import WwcApi from "../../WwcApi";


const EditNameModal = (props) => {
    // props: firstName, lastName, closeEditModal, submit

    const [userName, setUserName] = useState({
        first_name: props.firstName,
        last_name: props.lastName
    });

    // function to update user name data
    const handleChange = (event) => {
        let { name, value } = event.target;
        setUserName({ ...userName, [name]: value });
    };

    const handleSubmit = async (evt) => {
        evt.preventDefault();
        let result = {
            status: null,
            update: "name",
            nameInfo: null
        };
        try {
            const response = await WwcApi.editUserName(userName);
            result.status = "success"
            result.nameInfo = userName;

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
                    <div className={classes["modal-title-font"]}>Edit Profile Name</div>
                    <div className={classes["edit-instructions"]}>
                        <p>Click in any field to make changes</p>
                        <p className={classes['warning']} id='warning'>
                            *All fields are mandatory
                        </p>
                    </div>
                </header>
            </div>
            <div>
                <form onSubmit={handleSubmit}>
                    <div className={cx('form-group', styles['form-group'])}>
                        <label htmlFor='first_name'>First Name *</label>
                        <input
                            type='text'
                            name='first_name'
                            className={cx('form-control', styles['form-control'])}
                            id='first_name'
                            data-testid="edit-firstname"
                            aria-describedby='firstnameHelp'
                            defaultValue={props.firstName} // set to first name
                            onChange={handleChange}
                        />
                    </div>
                    <div className={cx('form-group', styles['form-group'])}>
                        <label htmlFor='last_name'>Last Name *</label>
                        <input
                            type='text'
                            name='last_name'
                            className={cx('form-control', styles['form-control'])}
                            id='last_name'
                            data-testid="edit-lastname"
                            aria-describedby='lastnameHelp'
                            defaultValue={props.lastName} // set to last name
                            onChange={handleChange}
                        />
                    </div>
                    {/* Confirm and cancel buttons */}
                    <div className='text-center'>
                            <button
                                type='submit'
                                className={cx('btn', classes['btn'], classes['confirm-btn'])}
                                data-testid='edit-name-submit-button'
                                disabled={
                                    props.firstName === userName.first_name &&
                                    props.lastName === userName.last_name
                                }
                            >
                            Confirm Changes
                            </button>
                            <button
                                className={cx('btn', classes['btn'], classes['cancel-btn'])}
                                data-testid='edit-name-cancel-button'
                                onClick={(e) => {e.preventDefault(); props.closeEditModal();}}
                            >
                            Cancel
                            </button>
                    </div>
                </form>
            </div>
        </div>
    );
};

export default EditNameModal;
