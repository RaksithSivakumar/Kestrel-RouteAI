export default function ReasonList({ reasons }: { reasons: string[] }) {
  if (!reasons.length) {
    return <p className="text-sm text-slate-500">No explanation was returned.</p>;
  }
  return (
    <ol className="list-decimal space-y-2 pl-5 text-sm text-kestrel-ink">
      {reasons.map((reason) => (
        <li key={reason}>{reason}</li>
      ))}
    </ol>
  );
}
