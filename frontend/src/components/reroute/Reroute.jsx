import React, { useContext } from "react";
import { Redirect } from "react-router-dom";
import AuthContext from "../../context/auth/AuthContext";

const Reroute = () => {
  const { token } = useContext(AuthContext);
  return token ? <Redirect to='/home' /> : <Redirect to='/login' />;
};

export default Reroute;
