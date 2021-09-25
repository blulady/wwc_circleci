import React, { useContext } from "react";
import { useHistory } from "react-router-dom";
import "./ContainerWithNav.css";
import AuthContext from "../../context/auth/AuthContext";
import WwcApi from "../../WwcApi";

/*
 * ContainerWithNav
 component with logo, title and profile icon. 
 * Profile icon contains drownload menu: email and logout.
 * This component also sets the base for all components.
 * provides the container and inner container for all its children.
 */
const ContainerWithNav = ({ children }) => {
  const history = useHistory();
  const { userInfo, handleRemoveAuth } = useContext(AuthContext);
  const userEmail = userInfo && "email" in userInfo ? userInfo.email : "";
  const firstNameInitial =
    userInfo && "first_name" in userInfo ? userInfo.first_name.slice(0, 1) : "";

  /*
   * Logout: remove userInfo, token in the context and redirect to login page
   */
  const handleLogout = async () => {
    try {
      await WwcApi.logout();
      handleRemoveAuth();
      history.push("/login");
    } catch (error) {
      console.log(error);
    }
  };

  const handleGoHome = () => {
    history.push("/home");
  }

  return (
    <div className='container-fluid'>
      <nav className='container-navbar'>
        <div className='container-inner'>
          <div className='navbar-wwc-logo navbar-brand'>
            <div className='logo-png' onClick={handleGoHome}></div>
          </div>
          <div className='navbar-items '>
            <ul className='navbar-items-ul'>
              <li className='navbar-items-wwc-title navbar-text'>
                Chapter Tools
              </li>
              <li className='navbar-items-user-button'>
                <div
                  className='user-button'
                  id='navbarDropdown'
                  role='button'
                  data-toggle='dropdown'
                  aria-haspopup='true'
                  aria-expanded='false'
                >
                  <span>{firstNameInitial}</span>
                </div>
                <div className='dropdown-menu' aria-labelledby='navbarDropdown'>

                  <p className='dropdown-item signed-user'>Signed-in as</p>
                  <p className='dropdown-item signed-user font-weight-bold'>{userEmail}</p>
                  <button
                    onClick={() => {
                      history.push({ pathname: "/member/profile" });
                    }}
                    className='dropdown-item item-profile'
                  >
                    Your Profile
                  </button>
                  <div className='dropdown-divider'></div>
                  <button
                    onClick={handleLogout}
                    className='dropdown-item item-logout'
                  >
                    Log Out
                  </button>
                </div>
              </li>
            </ul>
          </div>
        </div>
      </nav>
      <div className='container-body'>{children}</div>
    </div>
  );
};

export default ContainerWithNav;
