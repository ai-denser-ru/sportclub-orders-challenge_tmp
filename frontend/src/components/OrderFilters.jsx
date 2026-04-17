import { useSearchParams } from 'react-router-dom';

const STATUSES = ['', 'PENDING', 'PAID', 'CANCELLED'];
const STATUS_LABELS = { '': 'All Statuses', PENDING: 'Pending', PAID: 'Paid', CANCELLED: 'Cancelled' };

export default function OrderFilters() {
  const [searchParams, setSearchParams] = useSearchParams();

  const status = searchParams.get('status') || '';
  const dateFrom = searchParams.get('dateFrom') || '';
  const dateTo = searchParams.get('dateTo') || '';

  const updateFilter = (key, value) => {
    setSearchParams((prev) => {
      const next = new URLSearchParams(prev);
      if (value) {
        next.set(key, value);
      } else {
        next.delete(key);
      }
      return next;
    });
  };

  const clearFilters = () => {
    setSearchParams({});
  };

  const hasFilters = status || dateFrom || dateTo;

  return (
    <div className="rounded-xl border border-slate-800 bg-slate-900/60 p-4 backdrop-blur-sm">
      <div className="flex flex-wrap items-end gap-4">
        {/* Status */}
        <div className="flex flex-col gap-1.5 min-w-[160px]">
          <label className="text-xs font-medium text-slate-400 uppercase tracking-wider">
            Status
          </label>
          <select
            value={status}
            onChange={(e) => updateFilter('status', e.target.value)}
            className="rounded-lg border border-slate-700 bg-slate-800 px-3 py-2 text-sm text-slate-200 outline-none transition-colors focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500/50"
          >
            {STATUSES.map((s) => (
              <option key={s} value={s}>
                {STATUS_LABELS[s]}
              </option>
            ))}
          </select>
        </div>

        {/* Date From */}
        <div className="flex flex-col gap-1.5">
          <label className="text-xs font-medium text-slate-400 uppercase tracking-wider">
            From
          </label>
          <input
            type="date"
            value={dateFrom}
            onChange={(e) => updateFilter('dateFrom', e.target.value)}
            className="rounded-lg border border-slate-700 bg-slate-800 px-3 py-2 text-sm text-slate-200 outline-none transition-colors focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500/50"
          />
        </div>

        {/* Date To */}
        <div className="flex flex-col gap-1.5">
          <label className="text-xs font-medium text-slate-400 uppercase tracking-wider">
            To
          </label>
          <input
            type="date"
            value={dateTo}
            onChange={(e) => updateFilter('dateTo', e.target.value)}
            className="rounded-lg border border-slate-700 bg-slate-800 px-3 py-2 text-sm text-slate-200 outline-none transition-colors focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500/50"
          />
        </div>

        {/* Clear */}
        {hasFilters && (
          <button
            onClick={clearFilters}
            className="rounded-lg border border-slate-700 bg-slate-800 px-4 py-2 text-sm text-slate-400 transition-all hover:border-rose-500/50 hover:text-rose-400"
          >
            Clear filters
          </button>
        )}
      </div>
    </div>
  );
}
