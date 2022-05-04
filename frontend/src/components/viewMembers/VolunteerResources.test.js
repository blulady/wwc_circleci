import React from "react";
import { act, render, screen, fireEvent } from "@testing-library/react";
import VolunteerResources from "./VolunteerResources";
import AuthContext from "../../context/auth/AuthContext";
import {
  ERROR_VOLUNTEER_RESOURCES_DOCUMENT_NOT_LOADED,
  ERROR_VOLUNTEER_RESOURCES_NO_DOCUMENT_AVAILABLE,
} from "../../Messages";
import WwcApi from "../../WwcApi";

const userInfo = { userInfo: { role: "DIRECTOR" } };
jest.mock("../../WwcApi", () => {
  return {
    ...jest.requireActual("../../WwcApi"),
    getVolunteerResources: jest.fn(),
    updateVolunteerResources: jest.fn(),
  };
});

describe("Register Component Validation Tests", () => {
  beforeEach(() => {
    jest.resetAllMocks();
  });

  test("Tests VolunteerResources component behavior for GET resources", async () => {
    // Mock GET resources
    WwcApi.getVolunteerResources.mockImplementation(async () => {
      return await Promise.resolve({
        data: {
          edit_link: "test edit link",
          published_link: "test published link",
        },
      });
    });

    // WwcApi.updateVolunteerResources.mockImplementation(async () => {
    //   return await Promise.resolve({
    //     data: {
    //       edit_link: "test edit link",
    //       published_link: "test published link",
    //     },
    //   });
    // });

    await act(async () => {
      render(
        <AuthContext.Provider value={userInfo}>
          <VolunteerResources />
        </AuthContext.Provider>
      );
    });

    // form is rendered
    const editLink = screen.getByTestId("editLink");
    const publishedLink = screen.getByTestId("publishLink");
    expect(editLink.value).toBe("test edit link");
    expect(publishedLink.value).toBe("test published link");

    const saveBtn = screen.getByTestId("saveBtn");
    fireEvent.click(saveBtn);

    expect(() => screen.getByTestId("message-box")).toThrow(
      "Unable to find an element"
    );
  });

  test("Tests VolunteerResources component behavior for GET resources and fail on save", async () => {
    // Mock GET resources
    WwcApi.getVolunteerResources.mockImplementation(async () => {
      return await Promise.resolve({
        data: {
          edit_link: "test edit link",
          published_link: "test published link",
        },
      });
    });

    // Mock Update resources
    WwcApi.updateVolunteerResources.mockImplementation(async () => {
      return await Promise.reject(
        {
          response: {
            status: 404,
          },
        },
        404
      );
    });

    await act(async () => {
      render(
        <AuthContext.Provider value={userInfo}>
          <VolunteerResources />
        </AuthContext.Provider>
      );
    });

    // form is rendered
    const editLink = screen.getByTestId("editLink");
    const publishedLink = screen.getByTestId("publishLink");
    expect(editLink.value).toBe("test edit link");
    expect(publishedLink.value).toBe("test published link");

    const saveBtn = screen.getByTestId("saveBtn");

    await act(async () => {
      fireEvent.click(saveBtn);
    });

    await act(async () => {
      fireEvent.click(saveBtn);
    });

    expect(
      screen.getByText(ERROR_VOLUNTEER_RESOURCES_NO_DOCUMENT_AVAILABLE)
    ).toBeInTheDocument();
    expect(editLink.value).toBe("test edit link");
    expect(publishedLink.value).toBe("test published link");
  });

  test("Tests VolunteerResources component behavior for fetch failure", async () => {
    // Mock GET resources
    WwcApi.getVolunteerResources.mockImplementation(async () => {
      return await Promise.reject(
        {
          response: {
            status: 404,
          },
        },
        404
      );
    });
    await act(async () => {
      render(
        <AuthContext.Provider value={userInfo}>
          <VolunteerResources />
        </AuthContext.Provider>
      );
    });
    // Registration form is rendered
    const editLink = screen.getByTestId("editLink");
    const publishedLink = screen.getByTestId("publishLink");
    const messageBox = screen.getByTestId("message-box");
    expect(
      screen.getByText(ERROR_VOLUNTEER_RESOURCES_NO_DOCUMENT_AVAILABLE)
    ).toBeInTheDocument();
    // expect(editLink.value).toBe("test edit link");
    // expect(publishedLink.value).toBe("test published link");
  });
});
