import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import PredictionResult from "@/components/PredictionResult";
import ReasonList from "@/components/ReasonList";

describe("PredictionResult", () => {
  it("shows empty state", () => {
    render(<PredictionResult result={null} summary={null} />);
    expect(screen.getByText(/Submit a request on the left/i)).toBeInTheDocument();
  });

  it("renders a prediction", () => {
    render(
      <PredictionResult
        result={{
          request_id: "SR1",
          predicted_team: "Repairs",
          confidence_score: 0.81,
          relative_confidence: 0.7,
          score_type: "softmax_of_decision_function",
          reasons: ["The request describes a product fault or breakdown."],
        }}
        summary={{
          request_id: "SR1",
          request_text: "leaking water",
          product_family: "Water Purifier",
          warranty_status: "in_warranty",
          channel: "chat",
        }}
      />
    );
    expect(screen.getByText("Repairs")).toBeInTheDocument();
    expect(screen.getByText(/leaking water/)).toBeInTheDocument();
  });
});

describe("ReasonList", () => {
  it("lists reasons", () => {
    render(<ReasonList reasons={["Filter replacement"]} />);
    expect(screen.getByText("Filter replacement")).toBeInTheDocument();
  });
});
