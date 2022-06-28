import React from "react";
import { render } from "@testing-library/react";
import MessageBox from "./MessageBox";

describe("MessageBox", () => {
  test("it renders without crashing", () => {
    const { container } = render(
      <MessageBox
        type="Error"
        title="Sorry!"
        message="We could not process your request. \nPlease try again."
      />
    );
    expect(container).toMatchSnapshot();
  });

  test("it renders correct styling for error", () => {
    const { container } = render(
      <MessageBox
        type="Error"
        title="Sorry!"
        message="We could not process your request. \nPlease try again."
      />
    );
    const typeDiv = container.querySelector(".message-box");

    expect(typeDiv).toHaveClass("error");
  });

  test("it renders correct styling for success", () => {
    const { container } = render(
      <MessageBox
        type="Success"
        title="Success!"
        message="Request Completed."
      />
    );
    const typeDiv = container.querySelector(".message-box");

    expect(typeDiv).toHaveClass("success");
  });
});
