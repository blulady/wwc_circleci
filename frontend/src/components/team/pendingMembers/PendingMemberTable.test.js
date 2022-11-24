import React from "react";
import { render } from "@testing-library/react";
import PendingMemberTable from "./PendingMemberTable";

const pendingMembers = [{
    email: "abc@example.com",
    role_name: "volunteer",
    status: "invited"
}];

describe("PendingMemberTable Component Validation Tests", () => {
  test("PendingMemberTable component is rendering", async () => {
      const { container, getByText } = render(<PendingMemberTable users={pendingMembers} />);
      expect(container).toMatchSnapshot();

      expect(getByText("abc@example.com")).toBeTruthy();
      expect(getByText("volunteer")).toBeTruthy();
      expect(getByText("invited")).toBeTruthy();
  });
});
