import type { HealthResponse, PredictRequest, PredictResponse } from "@/types/prediction";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export async function getHealth(): Promise<HealthResponse> {
  const response = await fetch(`${API_URL}/health`, { cache: "no-store" });
  if (!response.ok) {
    throw new Error("Health check failed");
  }
  return response.json();
}

export async function predictRequest(payload: PredictRequest): Promise<PredictResponse> {
  const response = await fetch(`${API_URL}/predict`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  const body = await response.json().catch(() => ({}));
  if (!response.ok) {
    const detail = body.detail;
    const message =
      typeof detail === "string"
        ? detail
        : Array.isArray(detail)
          ? detail.map((item: { msg?: string }) => item.msg).join("; ")
          : `Routing service returned ${response.status}`;
    throw new Error(message);
  }
  return body as PredictResponse;
}

export { API_URL };
