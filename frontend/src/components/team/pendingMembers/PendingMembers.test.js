import React from "react";
import { render } from "@testing-library/react";
import WwcApi from "../../../WwcApi";
import PendingMembers from "./PendingMembers";

jest.mock("../../../WwcApi", () => {
  return {
    ...jest.requireActual("../../../WwcApi"),
    getPendingMembers: jest.fn(),
  };
});


describe("PendingMembers Component Validation Tests", () => {
  beforeEach(() => {
    jest.resetAllMocks();
  });

  test("PendingMembers component is rendering", async () => {
    // Mock GET resources
    WwcApi.getPendingMembers.mockImplementation(async () => {
      return await Promise.resolve({
        data: {
            email: "abc@example.com",
            role: "volunteer",
            status: "invited"
        },
      });
    });

    const { container } = render(
        <PendingMembers />
      );

    expect(container).toMatchSnapshot();

  });

  // Enable and test once BE is ready as some data is currently hard coded
//   test("PendingMembers component renders no invitess message", async () => {
//     // Mock GET resources
//     WwcApi.getPendingMembers.mockImplementation(async () => {
//         return await Promise.resolve({
//             data: {
//             email: "abc@example.com",
//             role: "volunteer",
//             status: "invited"
//             },
//         });
//     });
//     const { container, getByText } = render(
//         <PendingMembers />
//     );
//     expect(getByText("No invitees to display")).toBeTruthy();
//   });
});
