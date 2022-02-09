import React, { useState } from "react";
import styles from "./Register.module.css";
import cx from 'classnames';
import queryString from "query-string";
import { useHistory } from "react-router-dom";
import Password from "../layout/Password";
import Spinner from "../layout/Spinner";
import WwcApi from "../../WwcApi";

import MessageBox from "../messagebox/MessageBox";
import { ERROR_REGISTER_LINK_USED, ERROR_REGISTER_LINK_EXPIRED } from "../../Messages";


function Register(props) {
  const history = useHistory();
  const { email, token } = queryString.parse(props.location.search);
  const [errorOnLoading, setErrorOnLoading] = useState({hasError: false});
  const [processing, setProcessing] = useState(false);
  const [userInfo, setUserInfo] = useState({
    first_name: "",
    last_name: "",
    email,
    password: "",
    token,
  });

  // function to update user info fields
  const handleChange = (event) => {
    let { name, value } = event.target;
    setUserInfo({ ...userInfo, [name]: value });
  };

  const handleValidPwd = (pwd) => {
    setUserInfo({ ...userInfo, password: pwd });
  };

  // function to handle form submission
  const handleSubmit = async (e) => {
    e.preventDefault();
    setProcessing(true);
    const userData = { ...userInfo };
    try {
      await WwcApi.validateInvitation({params: {email, token}}); // check valid invitation
      try {
        await WwcApi.activateMember(userData); // activate member
        setProcessing(false);
        history.push("/login");
      } catch (error) { // error with activation
        setProcessing(false);
        setErrorOnLoading({hasError: true, title: "Oops!", message: ERROR_REGISTER_LINK_USED});
        console.log(error);
      }
    } catch (error) { // error with invitation
      setProcessing(false);
      setErrorOnLoading({hasError: true, title: "Sorry!", message: ERROR_REGISTER_LINK_EXPIRED});
    }
  };

  return (
    <div className={cx('container-fluid', styles['container'])}>
      <div className={styles['WwcLogo']}></div>
      <main>
        {errorOnLoading.hasError && (
          <MessageBox type="Error" title={errorOnLoading.title} message={errorOnLoading.message}></MessageBox>
        )}
        {processing && <Spinner />}
        {!errorOnLoading.hasError && !processing && (
          <div className={cx(styles['Register'], 'col col-md-6 col-lg-4')}>
            <header className="text-center">
              <div className={styles['title']}>Register for</div>
              <div className={styles['title']}>Chapter Tools</div>
              <p className={styles['warning']} id='warning'>
                *All fields are mandatory
              </p>
            </header>
            <div className={styles['register-form']}>
              <form onSubmit={handleSubmit}>
                <div className={cx('form-group', styles['form-group'])}>
                  <label htmlFor='first_name'>First Name *</label>
                  <input
                    type='text'
                    name='first_name'
                    className={cx('form-control', styles['form-control'])}
                    id='first_name'
                    data-testid="register-firstname"
                    aria-describedby='firstnameHelp'
                    value={userInfo.first_name}
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
                    data-testid="register-lastname"
                    aria-describedby='lastnameHelp'
                    value={userInfo.last_name}
                    onChange={handleChange}
                  />
                </div>
                <div className={cx('form-group', styles['form-group'])}>
                  <label htmlFor='Email'>Email address *</label>
                  <input
                    type='email'
                    name='email'
                    className={cx('form-control', styles['form-control'])}
                    id='Email'
                    data-testid = 'register-email'
                    aria-describedby='emailHelp'
                    value={userInfo.email}
                    readOnly
                  />
                </div>
                <Password setPwd={handleValidPwd} />
                <div className='text-center'>
                  <button
                    type='submit'
                    className={cx('btn', styles['btn'])}
                    data-testid='register-submit-button'
                    disabled={
                      !userInfo.password ||
                      !userInfo.first_name ||
                      !userInfo.last_name
                    }
                  >
                    Submit
                  </button>
                </div>
              </form>
            </div>
          </div>
        )} 
      </main>
    </div>
  );
}
export default Register;
