import ReasonList from "@/components/ReasonList";
import type { PredictRequest, PredictResponse } from "@/types/prediction";

export default function PredictionResult({
  result,
  summary,
}: {
  result: PredictResponse | null;
  summary: PredictRequest | null;
}) {
  if (!result) {
    return (
      <section className="rounded-lg border border-dashed border-kestrel-line bg-white p-6">
        <h2 className="text-lg text-kestrel-navy">Queue suggestion</h2>
        <p className="mt-3 text-sm leading-6 text-slate-600">
          Submit a request on the left. The desk will show the predicted team, a relative
          model score (not a calibrated probability), and short reasons a Kestrel agent can
          check.
        </p>
      </section>
    );
  }

  return (
    <section className="rounded-lg border border-kestrel-line bg-white p-6">
      <p className="text-xs uppercase tracking-[0.16em] text-kestrel-copper">Suggested queue</p>
      <h2 className="mt-2 text-2xl text-kestrel-navy">{result.predicted_team}</h2>
      <p className="mt-2 text-sm text-slate-600">
        Request {result.request_id} · relative confidence {result.relative_confidence.toFixed(2)} ·
        top-class score {result.confidence_score.toFixed(2)}
      </p>
      <p className="mt-1 text-xs text-slate-400">{result.score_type.replaceAll("_", " ")}</p>

      <div className="mt-5">
        <h3 className="mb-2 text-sm font-semibold text-kestrel-ink">Why this team</h3>
        <ReasonList reasons={result.reasons} />
      </div>

      {summary && (
        <div className="mt-6 border-t border-kestrel-line pt-4 text-sm">
          <h3 className="mb-2 font-semibold text-kestrel-ink">Request summary</h3>
          <dl className="grid grid-cols-3 gap-2 text-slate-600">
            <dt className="col-span-1">Product</dt>
            <dd className="col-span-2">{summary.product_family || "—"}</dd>
            <dt className="col-span-1">Warranty</dt>
            <dd className="col-span-2">{summary.warranty_status || "—"}</dd>
            <dt className="col-span-1">Channel</dt>
            <dd className="col-span-2">{summary.channel || "—"}</dd>
            <dt className="col-span-1">Text</dt>
            <dd className="col-span-2">{summary.request_text}</dd>
          </dl>
        </div>
      )}
    </section>
  );
}
