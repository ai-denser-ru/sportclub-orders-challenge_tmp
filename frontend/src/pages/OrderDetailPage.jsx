import { useParams, Link } from 'react-router-dom';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { fetchOrder, updateOrderStatus } from '../api/orders';
import StatusBadge from '../components/StatusBadge';
import Spinner from '../components/Spinner';

const NEXT_STATUS = {
  PENDING: ['PAID', 'CANCELLED'],
  PAID: ['CANCELLED'],
  CANCELLED: [],
};

const ACTION_STYLES = {
  PAID: 'bg-emerald-600 hover:bg-emerald-500 text-white',
  CANCELLED: 'bg-rose-600 hover:bg-rose-500 text-white',
};

export default function OrderDetailPage() {
  const { id } = useParams();
  const queryClient = useQueryClient();

  const {
    data: order,
    isLoading,
    isError,
    error,
  } = useQuery({
    queryKey: ['order', id],
    queryFn: () => fetchOrder(id),
  });

  const mutation = useMutation({
    mutationFn: updateOrderStatus,
    // Optimistic update
    onMutate: async ({ status: newStatus }) => {
      await queryClient.cancelQueries({ queryKey: ['order', id] });
      const previous = queryClient.getQueryData(['order', id]);
      queryClient.setQueryData(['order', id], (old) => ({
        ...old,
        status: newStatus,
      }));
      return { previous };
    },
    onError: (_err, _vars, context) => {
      if (context?.previous) {
        queryClient.setQueryData(['order', id], context.previous);
      }
    },
    onSettled: () => {
      queryClient.invalidateQueries({ queryKey: ['order', id] });
      queryClient.invalidateQueries({ queryKey: ['orders'] });
    },
  });

  if (isLoading) return <Spinner size="lg" />;

  if (isError) {
    return (
      <div className="space-y-4">
        <Link to="/orders" className="text-sm text-indigo-400 hover:text-indigo-300">
          ← Back to orders
        </Link>
        <div className="rounded-xl border border-rose-500/30 bg-rose-500/10 p-6 text-center text-rose-400">
          {error?.response?.status === 404
            ? `Order #${id} not found`
            : `Error: ${error?.message}`}
        </div>
      </div>
    );
  }

  const possibleNext = NEXT_STATUS[order.status] || [];

  return (
    <div className="space-y-6">
      {/* Back link */}
      <Link
        to="/orders"
        className="inline-flex items-center gap-1 text-sm text-indigo-400 transition-colors hover:text-indigo-300"
      >
        ← Back to orders
      </Link>

      {/* Header */}
      <div className="flex flex-wrap items-start justify-between gap-4">
        <div>
          <h1 className="text-3xl font-bold tracking-tight text-white">
            Order #{order.id}
          </h1>
          <p className="mt-1 text-sm text-slate-400">
            Placed on{' '}
            {new Date(order.date).toLocaleDateString('en-US', {
              weekday: 'long',
              year: 'numeric',
              month: 'long',
              day: 'numeric',
            })}
          </p>
        </div>
        <StatusBadge status={order.status} />
      </div>

      {/* Grid: Customer + Actions */}
      <div className="grid gap-6 md:grid-cols-2">
        {/* Customer Card */}
        <div className="rounded-xl border border-slate-800 bg-slate-900/60 p-6 backdrop-blur-sm">
          <h2 className="mb-4 text-sm font-semibold uppercase tracking-wider text-slate-400">
            Customer
          </h2>
          <div className="space-y-2">
            <p className="text-lg font-medium text-white">{order.customer.name}</p>
            <p className="text-sm text-slate-400">{order.customer.email}</p>
          </div>
        </div>

        {/* Actions Card */}
        <div className="rounded-xl border border-slate-800 bg-slate-900/60 p-6 backdrop-blur-sm">
          <h2 className="mb-4 text-sm font-semibold uppercase tracking-wider text-slate-400">
            Actions
          </h2>
          {possibleNext.length > 0 ? (
            <div className="flex flex-wrap gap-3">
              {possibleNext.map((nextStatus) => (
                <button
                  key={nextStatus}
                  disabled={mutation.isPending}
                  onClick={() => mutation.mutate({ id: order.id, status: nextStatus })}
                  className={`rounded-lg px-5 py-2.5 text-sm font-semibold transition-all disabled:opacity-50 ${ACTION_STYLES[nextStatus]}`}
                >
                  {mutation.isPending ? 'Updating…' : `Mark as ${nextStatus.toLowerCase()}`}
                </button>
              ))}
            </div>
          ) : (
            <p className="text-sm text-slate-500">
              No status transitions available.
            </p>
          )}
          {mutation.isError && (
            <p className="mt-3 text-sm text-rose-400">
              Failed to update: {mutation.error?.response?.data?.detail || mutation.error?.message}
            </p>
          )}
        </div>
      </div>

      {/* Items Table */}
      <div className="rounded-xl border border-slate-800 bg-slate-900/60 backdrop-blur-sm">
        <div className="border-b border-slate-800 px-6 py-4">
          <h2 className="text-sm font-semibold uppercase tracking-wider text-slate-400">
            Order Items
          </h2>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b border-slate-800/60 bg-slate-900/50">
                <th className="px-6 py-3 text-left text-xs font-semibold uppercase tracking-wider text-slate-400">
                  Product
                </th>
                <th className="px-6 py-3 text-center text-xs font-semibold uppercase tracking-wider text-slate-400">
                  Qty
                </th>
                <th className="px-6 py-3 text-right text-xs font-semibold uppercase tracking-wider text-slate-400">
                  Unit Price
                </th>
                <th className="px-6 py-3 text-right text-xs font-semibold uppercase tracking-wider text-slate-400">
                  Subtotal
                </th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/40">
              {order.items.map((item) => (
                <tr key={item.id} className="transition-colors hover:bg-slate-800/30">
                  <td className="px-6 py-3.5 text-sm text-slate-200">
                    {item.product_name}
                  </td>
                  <td className="px-6 py-3.5 text-center text-sm text-slate-300">
                    {item.quantity}
                  </td>
                  <td className="px-6 py-3.5 text-right text-sm text-slate-300">
                    ${item.price.toFixed(2)}
                  </td>
                  <td className="px-6 py-3.5 text-right text-sm font-medium text-white">
                    ${(item.quantity * item.price).toFixed(2)}
                  </td>
                </tr>
              ))}
            </tbody>
            <tfoot>
              <tr className="border-t border-slate-700 bg-slate-900/80">
                <td colSpan="3" className="px-6 py-4 text-right text-sm font-semibold uppercase tracking-wider text-slate-400">
                  Total
                </td>
                <td className="px-6 py-4 text-right text-lg font-bold text-indigo-400">
                  ${order.total.toFixed(2)}
                </td>
              </tr>
            </tfoot>
          </table>
        </div>
      </div>
    </div>
  );
}
