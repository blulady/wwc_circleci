import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Reroute from "./components/reroute/Reroute";
import Register from "./components/register/Register";
import Login from "./components/login/Login";
import ResetPasswordForm from "./components/resetpwform/ResetPasswordForm";
import Home from "./components/home/Home";
import NotFound from "./components/NotFound";
import AuthProvider from "./context/auth/AuthProvider";
import ReviewMember from "./components/addmember/ReviewMember";
import AddMember from "./components/addmember/AddMember";
import MemberDetails from "./components/memberdetails/MemberDetails";
import UserProfile from './components/userprofile/UserProfile'
import PrivateRoute from "./PrivateRoute";
import TeamHomeContainer from "./components/team/TeamHomeContainer";
import TeamResources from "./components/team/resources/TeamResources";
import ViewMembers from "./components/team/viewMembers/ViewMembers";
import PendingMembers from "./components/team/pendingMembers/PendingMembers";


function App() {
  return (
    <AuthProvider>
      <Router>
        <Routes>
          <Route exact path='/' element={<Reroute />} />
          <Route exact path='/login' element={<Login />} />
          <Route exact path='/password/reset' element={<ResetPasswordForm />} />
          <Route exact path='/home' element={<PrivateRoute element={<Home />}/>} />
          <Route path='/register' element={<Register />} />
          <Route path='/team/:team' element={<PrivateRoute element={<TeamHomeContainer />}/>}>
            <Route path='members' element={<ViewMembers />} />
            <Route path='pending' element={<PendingMembers />} />
            <Route path='resources' element={<TeamResources />} />
          </Route>
          <Route exact path='/member/view' element={<PrivateRoute element={<MemberDetails />}/>} />
          <Route exact path='/member/add' element={<PrivateRoute element={<AddMember />}/>} />
          <Route exact path='/member/review' element={<PrivateRoute element={<ReviewMember />}/>} />
          <Route exact path='/member/profile' element={<PrivateRoute element={<UserProfile />}/>} />
          <Route element={NotFound} />
        </Routes>
      </Router>
    </AuthProvider>
  );
}

export default App;
