import React, { useState } from "react";
import AuthContext from "./AuthContext";

const AuthProvider = ({ children }) => {
  const [token, setToken] = useState(
    JSON.parse(sessionStorage.getItem("token"))
  );
  const [userInfo, setUserInfo] = useState(
    JSON.parse(sessionStorage.getItem("user"))
  );

  /*
   * store token in session
   */
  const handleSetAuth = (token, user) => {
    sessionStorage.setItem("token", JSON.stringify(token));
    setToken(token);
    sessionStorage.setItem("user", JSON.stringify(user));
    setUserInfo(user);
  };

  // remove token from session
  const handleRemoveAuth = () => {
    sessionStorage.removeItem("token");
    sessionStorage.removeItem("user");
    setToken(null);
    setUserInfo(null);
  };

  return (
    <AuthContext.Provider
      value={{
        token,
        userInfo,
        handleSetAuth,
        handleRemoveAuth,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export default AuthProvider;
