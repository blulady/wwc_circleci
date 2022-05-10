import React, { useContext } from "react";
import { Navigate } from "react-router-dom";
import { useAuthContext } from "./context/auth/AuthContext";
import TeamProvider from "./context/team/TeamProvider";

const PrivateRoute = ({ element }) => {
  //const { token } = useContext(AuthContext);
  const { token } = useAuthContext();

  if (!token) {
    return <Navigate to='/login' />;
  }

  return (
    <TeamProvider>{element}</TeamProvider>   
  );
};

export default PrivateRoute;
