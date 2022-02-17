import React from "react";
import { render, screen, act, fireEvent } from "@testing-library/react";
import "@testing-library/jest-dom/extend-expect";
import MemberDetails from "./MemberDetails";
import AuthContext from "../../context/auth/AuthContext";
import { useLocation } from "react-router";
import WwcApi from "../../WwcApi";

jest.mock("react-router-dom", () => ({
  ...jest.requireActual("react-router-dom"),
  useLocation: () => ({
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
  }),
}));

jest.mock("../../WwcApi", () => {
  return {
    ...jest.requireActual("../../WwcApi"),
    getMember: async () => {
      return await Promise.resolve({
        date_joined: "2021-04-17T20:32:21.560122Z",
        email: "john.doe@gmail.com",
        first_name: "John",
        id: 15,
        last_name: "Doe",
        role: "VOLUNTEER",
        status: "ACTIVE",
        teams: [{ id: 1, name: "Event Volunteers" }],
      });
    },
    getTeams: async () => {
      return await Promise.resolve([
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
    },
  };
});

jest.mock("../layout/ContainerWithNav", function () {
  return {
    __esModule: true,
    default: ({ children }) => children,
  };
});

test("component is rendering", async () => {
  await act(async () => {
    render(
      <AuthContext.Provider value={userInfo}>
        <MemberDetails />
      </AuthContext.Provider>
    );
  });

  expect(screen.getByText("John Doe")).toBeTruthy();
  expect(screen.getByText("john.doe@gmail.com")).toBeTruthy();
  expect(screen.getByText("active")).toBeTruthy();
  expect(screen.getByText("Member Since April 17, 2021")).toBeTruthy();
  expect(screen.getByText("volunteer")).toBeTruthy();

  // if teams array isn't empty, can use screen.getByText("team name").toBeTruthy()
  expect(screen.getByText("Event Volunteers")).toBeTruthy();
});

test("change status to inactive by clicking slider", async () => {
  await act(async () => {
    render(
      <AuthContext.Provider value={userInfo}>
        <MemberDetails />
      </AuthContext.Provider>
    );
  });
  const button = screen.getByTestId("change-status-btn");
  fireEvent.click(button);
  expect(screen.getByText("inactive")).toBeTruthy();
  expect(button).not.toBeChecked();
});

test("opens edit teams form on btn click", async () => {
  let _container;
  await act(async () => {
    const { container } = render(
      <AuthContext.Provider value={userInfo}>
        <MemberDetails />
      </AuthContext.Provider>
    );
    _container = container;
  });
  const teamEditDiv = _container.querySelector("#team-edit");
  fireEvent.click(teamEditDiv);
  expect(screen.getByText("Assign Team(s)")).toBeTruthy();
});
