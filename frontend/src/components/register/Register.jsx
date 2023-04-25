import React, { useState, useEffect } from "react";
import styles from "./Register.module.css";
import cx from 'classnames';
import queryString from "query-string";
import { useNavigate, useSearchParams } from "react-router-dom";
import Password from "../layout/Password";
import Spinner from "../layout/Spinner";
import WwcApi from "../../WwcApi";

import MessageBox from "../messagebox/MessageBox";
import { ERROR_REQUEST_MESSAGE, ERROR_REGISTER_LINK_USED, ERROR_REGISTER_LINK_EXPIRED, ERROR_REGISTER_LINK_INVALID } from "../../Messages";


function Register(props) {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const email = searchParams.get("email");
  const token = searchParams.get("token");
  const [errorOnLoading, setErrorOnLoading] = useState({ hasError: false });
  const [processing, setProcessing] = useState(true);
  const [userInfo, setUserInfo] = useState({
    first_name: "",
    last_name: "",
    email,
    password: "",
    token,
  });

  React.useEffect( () => {
      (async function validate() {
        WwcApi.validateInvitation({ params: { email, token } }) // check valid invitation
          .then((res) => {
            setProcessing(false);
            if (res.data.detail.status !== "ACTIVE" && res.data.detail.status !== "VALID") {
              setErrorOnLoading({ hasError: true, title: "Oops!", message: res.data.detail.message });
            }
          })
          .catch((error) => {
            setErrorOnLoading({ hasError: true, title: "Sorry!", message: ERROR_REQUEST_MESSAGE }); // generic error
            setProcessing(false);
          });
      }());
  }, []); // only run once

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
      await WwcApi.activateMember(userData); // activate new member
      navigate("/login");
    } catch (error) { // error with activation
      setErrorOnLoading({ hasError: true, title: "Oops!", message: ERROR_REQUEST_MESSAGE }); // generic error
    } finally {
      setProcessing(false);
    }
  };

  return (
    <div className={cx('container-fluid', styles['container'])}>
      <div className={styles['WwcLogo']}></div>
      <main className={styles['register-main']}>
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
