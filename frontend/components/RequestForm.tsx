"use client";

import { FormEvent, useState } from "react";
import type { PredictRequest } from "@/types/prediction";

const PRODUCTS = [
  "Air Fryer",
  "Mixer Grinder",
  "Water Purifier",
  "Robot Vacuum",
  "Induction Cooktop",
  "Ceiling Fan",
  "Room Heater",
];

const CHANNELS = ["chat", "whatsapp", "ivr", "email"];
const WARRANTY = ["in_warranty", "out_of_warranty", "shield"];

export default function RequestForm({
  onSubmit,
  loading,
}: {
  onSubmit: (payload: PredictRequest) => void;
  loading: boolean;
}) {
  const [requestId, setRequestId] = useState("SR");
  const [text, setText] = useState("");
  const [product, setProduct] = useState("Water Purifier");
  const [warranty, setWarranty] = useState("in_warranty");
  const [channel, setChannel] = useState("chat");
  const [error, setError] = useState("");

  function handleSubmit(event: FormEvent) {
    event.preventDefault();
    if (!text.trim()) {
      setError("Enter the customer’s opening message or IVR transcript.");
      return;
    }
    setError("");
    onSubmit({
      request_id: requestId.trim() || "UNKNOWN",
      request_text: text.trim(),
      product_family: product,
      warranty_status: warranty,
      channel,
      source: "crm",
    });
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4 rounded-lg border border-kestrel-line bg-white p-6">
      <h2 className="text-lg text-kestrel-navy">New service request</h2>
      <label className="block text-sm">
        Request ID
        <input
          className="mt-1 w-full rounded border border-kestrel-line px-3 py-2"
          value={requestId}
          onChange={(e) => setRequestId(e.target.value)}
        />
      </label>
      <label className="block text-sm">
        Customer request
        <textarea
          className="mt-1 min-h-28 w-full rounded border border-kestrel-line px-3 py-2"
          value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder="Paste the opening chat, WhatsApp, email, or IVR text"
        />
      </label>
      <div className="grid gap-3 sm:grid-cols-3">
        <label className="text-sm">
          Product family
          <select
            className="mt-1 w-full rounded border border-kestrel-line px-3 py-2"
            value={product}
            onChange={(e) => setProduct(e.target.value)}
          >
            {PRODUCTS.map((item) => (
              <option key={item}>{item}</option>
            ))}
          </select>
        </label>
        <label className="text-sm">
          Warranty
          <select
            className="mt-1 w-full rounded border border-kestrel-line px-3 py-2"
            value={warranty}
            onChange={(e) => setWarranty(e.target.value)}
          >
            {WARRANTY.map((item) => (
              <option key={item}>{item}</option>
            ))}
          </select>
        </label>
        <label className="text-sm">
          Channel
          <select
            className="mt-1 w-full rounded border border-kestrel-line px-3 py-2"
            value={channel}
            onChange={(e) => setChannel(e.target.value)}
          >
            {CHANNELS.map((item) => (
              <option key={item}>{item}</option>
            ))}
          </select>
        </label>
      </div>
      {error ? <p className="text-sm text-red-700">{error}</p> : null}
      <button
        type="submit"
        disabled={loading}
        className="rounded bg-kestrel-navy px-4 py-2 text-sm text-white disabled:opacity-60"
      >
        {loading ? "Routing…" : "Route request"}
      </button>
    </form>
  );
}
