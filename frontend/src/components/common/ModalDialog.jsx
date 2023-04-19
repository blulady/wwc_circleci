import React from "react";
import cx from "classnames";
import classes from "./ModalDialog.module.css";
import { useRef } from "react";
import { useEffect } from "react";

const ModalDialog = (props) => {   
    const ref = useRef();
    
    useEffect(() => {
        if (props.onOpening) {
            ref.current.addEventListener("show.bs.modal", (event) => {
                let target = event.relatedTarget;
                props.onOpening(target);
            });
        }
    
        if (props.onClosing) {
            ref.current.addEventListener("hide.bs.modal", (event) => {
                let target = event.relatedTarget;
                props.onClosing(target);
            });
        }
    }, []);

    return (
        <div className="modal" id={props.id} tabIndex="-1" role="dialog" ref={ref}>
            <div className="modal-dialog modal-dialog-centered">
                <div className="modal-content">
                    <div className="modal-header font-weight-bold">
                        <header className="text-center">
                            <div className={classes["modal-title-text"]}>{props.title}</div>
                        </header>
                    </div>
                    <div className="modal-body">
                        <div className="mb-5">
                        {props.text}
                        </div>
                        <div className='text-center'>
                            <button
                                    className={cx('btn', classes['btn'], classes['cancel-btn'], classes["dialog-button"], "mr-3")}
                                    onClick={(e) => {e.preventDefault(); props.onCancel();}}
                                    data-bs-dismiss="modal"
                                >
                                Cancel
                            </button>
                            <button
                                type='submit'
                                className={cx('btn', classes['btn'], classes['confirm-btn'], classes["dialog-button"], classes["submit-button"])}
                                onClick={(e) => {e.preventDefault(); props.onConfirm();}} data-bs-dismiss="modal"
                            >
                                Confirm
                            </button>

                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default ModalDialog;
