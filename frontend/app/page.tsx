"use client";

import { useEffect, useState } from "react";
import RequestForm from "@/components/RequestForm";
import PredictionResult from "@/components/PredictionResult";
import { getHealth, predictRequest } from "@/lib/api";
import type { PredictRequest, PredictResponse } from "@/types/prediction";

export default function Page() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [result, setResult] = useState<PredictResponse | null>(null);
  const [summary, setSummary] = useState<PredictRequest | null>(null);
  const [backend, setBackend] = useState<"unknown" | "up" | "down">("unknown");

  useEffect(() => {
    getHealth()
      .then((health) => setBackend(health.model_loaded ? "up" : "down"))
      .catch(() => setBackend("down"));
  }, []);

  async function onSubmit(payload: PredictRequest) {
    setLoading(true);
    setError("");
    try {
      const prediction = await predictRequest(payload);
      setResult(prediction);
      setSummary(payload);
      setBackend("up");
    } catch (err) {
      setResult(null);
      setError(err instanceof Error ? err.message : "Routing failed");
      setBackend("down");
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="mx-auto grid max-w-6xl gap-6 px-6 py-8 lg:grid-cols-2">
      <div>
        <p className="mb-3 text-xs uppercase tracking-[0.14em] text-slate-500">
          Backend:{" "}
          {backend === "up" ? "connected" : backend === "down" ? "unavailable" : "checking…"}
        </p>
        <RequestForm onSubmit={onSubmit} loading={loading} />
        {error ? (
          <p className="mt-3 rounded border border-red-200 bg-red-50 px-3 py-2 text-sm text-red-800">
            {error}. Confirm the FastAPI service is running on port 8000.
          </p>
        ) : null}
      </div>
      <PredictionResult result={result} summary={summary} />
    </main>
  );
}
