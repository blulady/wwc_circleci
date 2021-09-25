import React from "react";
import { BrowserRouter as Router, Route, Switch } from "react-router-dom";
import Reroute from "./components/reroute/Reroute";
import Register from "./components/register/Register";
import Login from "./components/login/Login";
import ResetPasswordForm from "./components/resetpwform/ResetPasswordForm";
import Home from "./components/home/Home";
import NotFound from "./components/NotFound";
import AuthProvider from "./context/auth/AuthProvider";
import ViewMembers from "./components/viewMembers/ViewMembers";
import ReviewMember from "./components/addmember/ReviewMember";
import AddMember from "./components/addmember/AddMember";
import ViewMemberDetails from "./components/memberdetails/ViewMemberDetails";
import UserProfile from './components/userProfile/UserProfile'
import PrivateRoute from "./PrivateRoute";
import VolunteerResources from "./components/viewMembers/VolunteerResources";
import ChapterMembersContainer from "./components/viewMembers/ChapterMembersContainer";

function App() {
  return (
    <AuthProvider>
      <Router>
        <Switch>
          <Route exact path='/' component={Reroute} />
          <Route exact path='/login' component={Login} />
          <Route exact path='/password/reset' component={ResetPasswordForm} />
          <PrivateRoute exact path='/home'>
            <Home />
          </PrivateRoute>
          <Route path='/register' component={Register} />
          <PrivateRoute exact path='/members/volunteerresources'>
            <VolunteerResources />
          </PrivateRoute>
          <PrivateRoute exact path='/members/chaptermembers'>
            <ChapterMembersContainer />
          </PrivateRoute>
          <PrivateRoute exact path='/members/viewall'>
            <ViewMembers />
          </PrivateRoute>
          <PrivateRoute exact path='/member/view'>
            <ViewMemberDetails />
          </PrivateRoute>
          <PrivateRoute exact path='/member/add'>
            <AddMember />
          </PrivateRoute>
          <PrivateRoute exact path='/member/review'>
            <ReviewMember />
          </PrivateRoute>
          <PrivateRoute exact path='/member/profile'>
            <UserProfile />
          </PrivateRoute>
          <Route component={NotFound} />
        </Switch>
      </Router>
    </AuthProvider>
  );
}

export default App;
