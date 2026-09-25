import { fireEvent, render, screen } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";
import RequestForm from "@/components/RequestForm";

describe("RequestForm", () => {
  it("renders intake fields", () => {
    render(<RequestForm onSubmit={vi.fn()} loading={false} />);
    expect(screen.getByText("New service request")).toBeInTheDocument();
    expect(screen.getByText("Customer request")).toBeInTheDocument();
    expect(screen.getByText("Route request")).toBeInTheDocument();
  });

  it("blocks empty text", async () => {
    const onSubmit = vi.fn();
    render(<RequestForm onSubmit={onSubmit} loading={false} />);
    fireEvent.submit(screen.getByRole("button", { name: "Route request" }).closest("form") as HTMLFormElement);
    expect(onSubmit).not.toHaveBeenCalled();
    expect(screen.getByText(/opening message/i)).toBeInTheDocument();
  });
});
