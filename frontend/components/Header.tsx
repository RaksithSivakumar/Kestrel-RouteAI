export default function Header() {
  return (
    <header className="border-b border-kestrel-line bg-white">
      <div className="mx-auto flex max-w-6xl items-end justify-between px-6 py-5">
        <div>
          <p className="text-xs uppercase tracking-[0.18em] text-kestrel-copper">
            Kestrel Home Appliances
          </p>
          <h1 className="mt-1 font-sans text-2xl text-kestrel-ink">RouteAI desk</h1>
          <p className="mt-1 text-sm text-slate-600">
            Internal routing for inbound service requests — Pune D2C operations
          </p>
        </div>
        <p className="hidden text-right text-xs text-slate-500 sm:block">
          Offline model · no per-ticket API bill
        </p>
      </div>
    </header>
  );
}
