import { describe, expect, it, vi, beforeEach } from "vitest";
import { predictRequest } from "@/lib/api";

describe("api client", () => {
  beforeEach(() => {
    vi.stubGlobal("fetch", vi.fn());
  });

  it("posts a prediction", async () => {
    vi.mocked(fetch).mockResolvedValue({
      ok: true,
      json: async () => ({
        request_id: "SR1",
        predicted_team: "Billing",
        confidence_score: 0.9,
        relative_confidence: 0.8,
        score_type: "softmax_of_decision_function",
        reasons: ["invoice"],
      }),
    } as Response);
    const result = await predictRequest({
      request_id: "SR1",
      request_text: "gst invoice",
      product_family: "Air Fryer",
      warranty_status: "in_warranty",
      channel: "email",
    });
    expect(result.predicted_team).toBe("Billing");
  });

  it("surfaces API errors", async () => {
    vi.mocked(fetch).mockResolvedValue({
      ok: false,
      status: 503,
      json: async () => ({ detail: "model missing" }),
    } as Response);
    await expect(
      predictRequest({
        request_id: "SR1",
        request_text: "help",
        product_family: "Air Fryer",
        warranty_status: "in_warranty",
        channel: "chat",
      })
    ).rejects.toThrow(/model missing/);
  });
});
