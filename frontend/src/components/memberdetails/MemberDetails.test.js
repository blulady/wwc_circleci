import React from "react";
import { render, screen, act, fireEvent } from "@testing-library/react";
import "@testing-library/jest-dom/extend-expect";
import MemberDetails from "./MemberDetails";
import { useLocation } from "react-router";
import WwcApi from "../../WwcApi";

jest.mock("react-router");
jest.mock("../../WwcApi");

useLocation.mockReturnValue({
  pathname: "/member/view",
  hash: "",
  key: "3v7zjr",
  search: "",
  state: {
    date_joined: "2021-04-17T20:32:21.560122Z",
    email: "wwctestvol1@gmail.com",
    first_name: "TestVolunteer",
    id: 64,
    last_name: "Volunteer1",
    role: "VOLUNTEER",
    status: "ACTIVE",
    teams: [],
  },
});

WwcApi.getMember.mockResolvedValue({
  date_joined: "2021-04-17T20:32:21.560122Z",
  email: "john.doe@gmail.com",
  first_name: "John",
  id: 15,
  last_name: "Doe",
  role: "VOLUNTEER",
  status: "ACTIVE",
  teams: [],
});

WwcApi.getTeams.mockResolvedValue([
  [
    { id: 1, name: "Event Volunteers" },
    { id: 2, name: "Hackathon Volunteers" },
    { id: 3, name: "Host Management" },
    { id: 4, name: "Partnership Management" },
    { id: 5, name: "Social Media" },
    { id: 6, name: "Tech Event Volunteers" },
    { id: 7, name: "Volunteer Management" },
  ],
]);

jest.mock("../layout/ContainerWithNav", function () {
  return {
    __esModule: true,
    default: ({ children }) => children,
  };
});

test("component is rendering", async () => {
  await act(async () => {
    render(<MemberDetails />);
  });

  expect(screen.getByText("John Doe")).toBeTruthy();
  expect(screen.getByText("john.doe@gmail.com")).toBeTruthy();
  expect(screen.getByText("Active")).toBeTruthy();
  expect(screen.getByText("Member Since April 17, 2021")).toBeTruthy();
  expect(screen.getByText("Volunteer")).toBeTruthy();
  
  // if teams array isn't empty, can use sscreen.getByText("team name").toBeTruthy()
  expect(screen.getByTestId("teams")).toHaveTextContent("");
});

test("opens edit status/role form on edit status click", async () => {
  await act(async () => {
    render(<MemberDetails />);
  });
  const button = screen.getByAltText("Edit-status");
  fireEvent.click(button);
  expect(screen.getByTestId("edit-role-status")).toBeTruthy();
});

test("opens edit status/role form on edit role click", async () => {
  await act(async () => {
    render(<MemberDetails />);
  });
  const button = screen.getByAltText("Edit-role");
  fireEvent.click(button);
  expect(screen.getByTestId("edit-role-status")).toBeTruthy();
}); 

test("opens edit teams form on btn click", async () => {
  await act(async () => {
    render(<MemberDetails />);
  });
  const button = screen.getByAltText("Edit-team");
  fireEvent.click(button);
  expect(screen.getByTestId("edit-teams")).toBeTruthy();
})
