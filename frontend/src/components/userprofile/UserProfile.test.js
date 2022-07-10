import React from "react";
import { render, screen, act, fireEvent } from "@testing-library/react";
import "@testing-library/jest-dom/extend-expect";
import UserProfile from "./UserProfile";
import AuthContext from "../../context/auth/AuthContext";


const mockNavigation = jest.fn();

const userInfo = { userInfo: {} };

jest.mock("react-router-dom", () => ({
    ...jest.requireActual("react-router-dom"),
    useNavigate: () => mockNavigation,
    useLocation: () => ({
        pathname: "/member/profile",
        hash: "",
        key: "3v7zjr",
        search: "",
        state: {
            "id": 2,
            "first_name": "Alice",
            "last_name": "Robinson",
            "email": "volunteer@example.com",
            "status": "ACTIVE",
            "highest_role": "VOLUNTEER",
            "date_joined": "2021-02-19T01:56:06.115000Z",
            "role_teams": [
            {
                "team_id": 4,
                "team_name": "Partnership Management",
                "role_name": "VOLUNTEER"
            },
            {
                "team_id": 5,
                "team_name": "Social Media",
                "role_name": "VOLUNTEER"
            },
            {
                "team_id": 3,
                "team_name": "Host Management",
                "role_name": "VOLUNTEER"
            },
            {
                "role_name": "VOLUNTEER"
            }
            ]
        },
    }),
}));


jest.mock("../../WwcApi", () => {
    return {
        ...jest.requireActual("../../WwcApi"),
        getUserProfile: async () => {
        return await Promise.resolve({
            "id": 2,
            "first_name": "Alice",
            "last_name": "Robinson",
            "email": "volunteer@example.com",
            "status": "ACTIVE",
            "highest_role": "VOLUNTEER",
            "date_joined": "2021-02-19T01:56:06.115000Z",
            "role_teams": [
            {
                "team_id": 4,
                "team_name": "Partnership Management",
                "role_name": "VOLUNTEER"
            },
            {
                "team_id": 5,
                "team_name": "Social Media",
                "role_name": "VOLUNTEER"
            },
            {
                "team_id": 3,
                "team_name": "Host Management",
                "role_name": "VOLUNTEER"
            },
            {
                "role_name": "VOLUNTEER"
            }
            ]
        });
        },
        editUserName: async (userName) => {
            return await Promise.resolve();
        },
        editUserPassword: async (data) => {
            return await Promise.resolve();
        }
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
            <UserProfile />
        </AuthContext.Provider>
        );
    });
    
    expect(screen.getByText("Alice Robinson")).toBeTruthy();
    expect(screen.getByText("volunteer@example.com")).toBeTruthy();
    expect(screen.getByText("active")).toBeTruthy();
    expect(screen.getByText("Member Since February 19, 2021")).toBeTruthy();
    expect(screen.getByText("volunteer")).toBeTruthy();
    expect(screen.getByText("Partnership Management")).toBeTruthy();
});


test("it renders name change form and updates name", async () => {
    await act(async () => {
        render(
        <AuthContext.Provider value={userInfo}>
            <UserProfile />
        </AuthContext.Provider>
        );
    });

    const button = screen.getByTestId("change-name-icon");
    fireEvent.click(button);
    expect(screen.getByText("Edit Profile Name")).toBeTruthy();
    const firstNameField = screen.getByTestId("edit-firstname");
    fireEvent.change(firstNameField, {target: {value: 'Alice1'}});
    const confirmButton = screen.getByTestId("edit-name-submit-button");
    await act(async() => {fireEvent.click(confirmButton)});
    expect(screen.getByText("Alice1 Robinson")).toBeTruthy();
});


test("it renders password change form and updates password", async () => {
    await act(async () => {
        render(
        <AuthContext.Provider value={userInfo}>
            <UserProfile />
        </AuthContext.Provider>
        );
    });

    const button = screen.getByTestId("change-password-button");
    fireEvent.click(button);
    expect(screen.getByText("Edit Password")).toBeTruthy();
    const passwordField = screen.getByTestId("password");
    fireEvent.change(passwordField, {target: {value: 'Password321'}});
    const confirmButton = screen.getByTestId("edit-pw-submit-button");
    await act(async() => {fireEvent.click(confirmButton)});
    expect(screen.getByText("Changes to your profile have been saved.")).toBeTruthy();
});
