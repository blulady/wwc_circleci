import React, { useContext } from "react";
import { Route, Redirect } from "react-router-dom";
import AuthContext from "./context/auth/AuthContext";

const PrivateRoute = ({ exact, path, children }) => {
  const { token } = useContext(AuthContext);

  if (!token) {
    return <Redirect to='/login' />;
  }

  return (
    <Route exact={exact} path={path}>
      {children}
    </Route>
  );
};

export default PrivateRoute;
