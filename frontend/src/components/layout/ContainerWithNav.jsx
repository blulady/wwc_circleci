import React, { useContext } from "react";
import { useNavigate } from "react-router-dom";
import styles from "./ContainerWithNav.module.css";
import cx from 'classnames';
import { useAuthContext } from "../../context/auth/AuthContext";
import WwcApi from "../../WwcApi";

/*
 * ContainerWithNav
 component with logo, title and profile icon. 
 * Profile icon contains drownload menu: email and logout.
 * This component also sets the base for all components.
 * provides the container and inner container for all its children.
 */
const ContainerWithNav = ({ children }) => {
  const navigate = useNavigate();
  const { userInfo, handleRemoveAuth } = useAuthContext();
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
      navigate("/login");
    } catch (error) {
      console.log(error);
    }
  };

  const handleGoHome = () => {
    navigate("/home");
  }

  return (
    <div className={cx('container-fluid', styles['container-fluid'])}>
      <nav className={styles['container-navbar']}>
        <div className={styles['container-inner']}>
          <div className={cx('navbar-brand', styles['navbar-wwc-logo'], )}>
            <div className={styles['logo-png']} onClick={handleGoHome}></div>
          </div>
          <div className={styles['navbar-items ']}>
            <ul className={styles['navbar-items-ul']}>
              <li className={cx('navbar-text', styles['navbar-items-wwc-title'])}>
                Chapter Tools
              </li>
              <li className={styles['navbar-items-user-button']}>
                <div
                  className={styles['user-button']}
                  id='navbarDropdown'
                  role='button'
                  data-bs-toggle='dropdown'
                  aria-haspopup='true'
                  aria-expanded='false'
                >
                  <span>{firstNameInitial}</span>
                </div>
                <div className={cx('dropdown-menu', styles['dropdown-menu' ])} aria-labelledby='navbarDropdown'>

                  <p className={cx('dropdown-item', styles['signed-user'] ,styles['dropdown-item'])}>Signed-in as</p>
                  <p className={cx('font-weight-bold dropdown-item',styles['signed-user'], styles['dropdown-item'])}>{userEmail}</p>
                  <button
                    onClick={() => {
                      navigate("/member/profile");
                    }}
                    className={cx('dropdown-item', styles['dropdown-item'])}
                  >
                    Your Profile
                  </button>
                  <hr className={cx('dropdown-divider', styles['dropdown-hr'])} />
                  <button
                    onClick={handleLogout}
                    className={cx('dropdown-item', styles['item-logout'], styles['dropdown-item'])}
                  >
                    Log Out
                  </button>
                </div>
              </li>
            </ul>
          </div>
        </div>
      </nav>
      <div className={styles['container-body']}>{children}</div>
    </div>
  );
};

export default ContainerWithNav;
