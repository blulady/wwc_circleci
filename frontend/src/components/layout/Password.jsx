import React, { useState, useEffect } from "react";
import cancelIcon from "../../images/cancel_24px.png";
import checkIcon from "../../images/check_circle_24px.png";
import styles from "./Password.module.css";
import cx from 'classnames';

const Password = ({ setPwd , pwdLabel= "Password *"}) => {
  const [password, setPassword] = useState("");
  const [hidden, setHidden] = useState(true);
  const [pwdValidation, setPwdValidation] = useState(false);
  const passwordValidationDescriptions = [
    "8-50 characters",
    "At least  1 upper case letter",
    "At least 1 lower case letter",
    "At least 1 numeric character",
  ];
  const [passwdValidStatus, setPasswdValidStatus] = useState([
    false,
    false,
    false,
    false,
  ]);

  useEffect(() => {
    checkValidation();
  }, [password]);

  // function for validating password
  const validatePassword = (e) => {
    const regexs = [
      RegExp(/^(?=.{8,50}$)/),
      RegExp(/(?=.*[A-Z])/),
      RegExp(/(?=.*[a-z])/),
      RegExp(/(?=.*[0-9])/),
    ];
    const validStatus = regexs.map((regex) => regex.test(e.target.value));
    setPasswdValidStatus(() => validStatus);
    setPassword(e.target.value);
  };
  // function to handle show/hide toggle
  const handleShow = (e) => {
    setHidden(!hidden);
  };

  const checkValidation = () => {
    if (passwdValidStatus.every((val) => val === true)) {
      setPwd(password);
    } else {
      setPwd("");
    }
  };

  return (
    <div className='form-group' onFocus={() => setPwdValidation(true)}>
      <label className={cx('pb-1', styles['label'])} htmlFor='Password'>{pwdLabel}</label>
      <div>
        <div className='input-group'>
          <input
            type={hidden ? "password" : "text"}
            name='password'
            className={cx('form-control', styles['input-pwd'])}
            data-testid="password"
            id='password'
            value={password}
            autoComplete="password"
            onChange={validatePassword}
          />
          <div className='input-group-append'>
            <span className={cx('input-group-text', styles['show-hide'])} onClick={handleShow}>
              <u data-testid="show-hide">{hidden ? "SHOW" : "HIDE"}</u>
            </span>
          </div>
        </div>
      </div>
      <div className={styles.validations}>
        <aside className={pwdValidation ? styles['display-inline'] : styles['display-none'] }>
          {passwdValidStatus.map((x, idx) => {
            const iconSrc = x ? checkIcon : cancelIcon;
            return (
              <div key={idx}>
                <img
                  src={iconSrc}
                  alt='Invalid Password Icon'
                  className={styles['validation-img']}
                />
                <span className={styles.pwddesc}>
                  {passwordValidationDescriptions[idx]}
                </span>
              </div>
            );
          })}
        </aside>
      </div>
    </div>
  );
};

export default Password;
