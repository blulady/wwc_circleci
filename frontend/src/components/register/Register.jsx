import React, { useState } from "react";
import "./Register.css";
import queryString from "query-string";
import { useHistory } from "react-router-dom";
import Password from "../layout/Password";
import WwcApi from "../../WwcApi";

function Register(props) {
  const history = useHistory();
  const { email, token } = queryString.parse(props.location.search);
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
    const userData = { ...userInfo };
    try {
      await WwcApi.register(userData);
      alert("member successfully added");
      history.push("/login");
    } catch (error) {
      alert(error + ':\n' +JSON.stringify(error.response.data))
    }
  };

  return (
    <div className='container'>
      <div className='WwcLogo'></div>
      <main>
        <div className='Register col col-md-6 col-lg-4'>
          <header>
            <div className='title'>Register for</div>
            <div className='title'>Chapter Tools</div>
            <p className='warning' id='warning'>
              *All fields are mandatory
            </p>
          </header>
          <div className='register-form'>
            <form onSubmit={handleSubmit}>
              <div className='form-group'>
                <label htmlFor='first_name'>First Name *</label>
                <input
                  type='text'
                  name='first_name'
                  className='form-control'
                  id='first_name'
                  data-testid="register-firstname"
                  aria-describedby='firstnameHelp'
                  value={userInfo.first_name}
                  onChange={handleChange}
                />
              </div>
              <div className='form-group'>
                <label htmlFor='last_name'>Last Name *</label>
                <input
                  type='text'
                  name='last_name'
                  className='form-control'
                  id='last_name'
                  data-testid="register-lastname"
                  aria-describedby='lastnameHelp'
                  value={userInfo.last_name}
                  onChange={handleChange}
                />
              </div>
              <div className='form-group'>
                <label htmlFor='Email'>Email address *</label>
                <input
                  type='email'
                  name='email'
                  className='form-control'
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
                  className='btn'
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
      </main>
    </div>
  );
}
export default Register;
