import React, { useContext } from "react";
import { Navigate } from "react-router-dom";
import AuthContext from "../../context/auth/AuthContext";

const Reroute = () => {
  const { token } = useContext(AuthContext);
  return token ? <Navigate to='/home' /> : <Navigate to='/login' />;
};

export default Reroute;
