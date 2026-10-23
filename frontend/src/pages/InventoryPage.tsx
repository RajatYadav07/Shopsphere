import React, { useEffect, useState } from 'react';
import {
  Layers,
  ArrowUpRight,
  ArrowDownRight,
  AlertTriangle,
  Package,
  Plus,
  Minus,
  RefreshCw,
  Search,
  ChevronLeft,
  ChevronRight,
  Check,
  X,
  Info
} from 'lucide-react';
import { apiClient } from '../api/client';
import { InventoryMovement, PaginatedResult, Product } from '../types';
import { Modal } from '../components/Modal';
import { LoadingState } from '../components/EmptyState';

export const InventoryPage: React.FC = () => {
  const [summary, setSummary] = useState<any>(null);
  const [movements, setMovements] = useState<InventoryMovement[]>([]);
  const [totalMovements, setTotalMovements] = useState<number>(0);
  const [page, setPage] = useState<number>(1);
  const [pageSize] = useState<number>(15);
  const [totalPages, setTotalPages] = useState<number>(1);
  const [loading, setLoading] = useState<boolean>(true);

  // Products for adjustment modal
  const [allProducts, setAllProducts] = useState<Product[]>([]);
  const [isAdjustModalOpen, setIsAdjustModalOpen] = useState<boolean>(false);
  const [adjustProductId, setAdjustProductId] = useState<string>('');
  const [adjustType, setAdjustType] = useState<'stock_in' | 'stock_out'>('stock_in');
  const [adjustQty, setAdjustQty] = useState<number>(10);
  const [adjustReason, setAdjustReason] = useState<string>('Warehouse restocking intake');
  const [actionSuccess, setActionSuccess] = useState<string | null>(null);
  const [actionError, setActionError] = useState<string | null>(null);

  const fetchInventoryData = async () => {
    try {
      setLoading(true);
      const [sumRes, movRes, pRes] = await Promise.all([
        apiClient.get('/inventory/summary'),
        apiClient.get('/inventory/movements', { params: { page, page_size: pageSize } }),
        apiClient.get('/products?page=1&page_size=100'),
      ]);
      setSummary(sumRes.data?.data || null);
      const movData: PaginatedResult<InventoryMovement> = movRes.data;
      setMovements(movData.items || []);
      setTotalMovements(movData.total || 0);
      setTotalPages(movData.total_pages || 1);
      const prods = pRes.data?.items || [];
      setAllProducts(prods);
      if (prods.length > 0 && !adjustProductId) {
        setAdjustProductId(prods[0].id);
      }
    } catch (e) {
      console.error('Error fetching inventory data:', e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchInventoryData();
  }, [page]);

  const handleAdjustStock = async (e: React.FormEvent) => {
    e.preventDefault();
    setActionError(null);

    const changeQty = adjustType === 'stock_in' ? Math.abs(adjustQty) : -Math.abs(adjustQty);

    try {
      await apiClient.post('/inventory/adjust', {
        product_id: adjustProductId,
        change_quantity: changeQty,
        reason: adjustReason,
      });
      setIsAdjustModalOpen(false);
      setActionSuccess(`Stock adjusted by ${changeQty > 0 ? `+${changeQty}` : changeQty} units. Movement logged in MongoDB.`);
      fetchInventoryData();
      setTimeout(() => setActionSuccess(null), 5000);
    } catch (err: any) {
      setActionError(err.message || 'Stock adjustment rejected');
    }
  };

  return (
    <div className="space-y-6">
      {/* Top Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 bg-white p-5 rounded-2xl border border-slate-200/80 shadow-subtle">
        <div>
          <h2 className="text-xl font-bold text-slate-900 tracking-tight">Inventory &amp; Audit Trail</h2>
          <p className="text-xs text-slate-500 mt-0.5">
            Immutable inventory movements logged in MongoDB with reason &amp; order audit tracking.
          </p>
        </div>
        <div className="flex items-center gap-2">
          <button
            onClick={() => setIsAdjustModalOpen(true)}
            className="flex items-center gap-1.5 px-4 py-2 bg-brand-600 hover:bg-brand-700 text-white rounded-xl text-xs font-semibold shadow-sm transition"
          >
            <Plus className="w-4 h-4" />
            <span>Adjust Stock (In / Out)</span>
          </button>
        </div>
      </div>

      {actionSuccess && (
        <div className="p-3 bg-emerald-50 border border-emerald-200 text-emerald-800 rounded-xl text-xs flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Check className="w-4 h-4 text-emerald-600" />
            <span className="font-medium">{actionSuccess}</span>
          </div>
          <button onClick={() => setActionSuccess(null)}>
            <X className="w-4 h-4 text-emerald-600" />
          </button>
        </div>
      )}

      {summary?.notice && (
        <div className="p-4 bg-blue-50/80 border border-blue-200/80 rounded-2xl text-xs text-blue-900 flex items-start gap-3">
          <Info className="w-5 h-5 text-blue-600 shrink-0 mt-0.5" />
          <div>
            <h4 className="font-bold text-blue-950">Olist Historical Inventory Architecture</h4>
            <p className="mt-0.5 text-blue-800 leading-relaxed">{summary.notice}</p>
            <div className="flex flex-wrap gap-4 mt-2 font-medium">
              <span>Historical Catalog SKUs: <strong className="text-blue-950">{summary.historical_catalog_count?.toLocaleString()}</strong></span>
              <span>Operational Tracked SKUs: <strong className="text-blue-950">{summary.tracked_inventory_count?.toLocaleString()}</strong></span>
            </div>
          </div>
        </div>
      )}

      {/* KPI Stats */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="bg-white p-5 rounded-xl border border-slate-200/80 shadow-subtle">
          <p className="text-xs font-medium uppercase text-slate-500">Warehouse Stock</p>
          <h3 className="text-2xl font-bold text-slate-900 mt-1">
            {summary?.total_units_in_stock?.toLocaleString() || 0}
          </h3>
          <p className="text-xs text-slate-500 mt-1">Total physical units</p>
        </div>

        <div className="bg-white p-5 rounded-xl border border-slate-200/80 shadow-subtle">
          <p className="text-xs font-medium uppercase text-slate-500">Low Stock SKUs</p>
          <h3 className="text-2xl font-bold text-amber-600 mt-1">
            {summary?.low_stock_count || 0}
          </h3>
          <p className="text-xs text-slate-500 mt-1">&lt;= 10 units remaining</p>
        </div>

        <div className="bg-white p-5 rounded-xl border border-slate-200/80 shadow-subtle">
          <p className="text-xs font-medium uppercase text-slate-500">Out of Stock</p>
          <h3 className="text-2xl font-bold text-rose-600 mt-1">
            {summary?.out_of_stock_count || 0}
          </h3>
          <p className="text-xs text-slate-500 mt-1">Zero units remaining</p>
        </div>

        <div className="bg-white p-5 rounded-xl border border-slate-200/80 shadow-subtle">
          <p className="text-xs font-medium uppercase text-slate-500">Audit Trail Events</p>
          <h3 className="text-2xl font-bold text-brand-600 mt-1">
            {summary?.total_movement_records || totalMovements}
          </h3>
          <p className="text-xs text-slate-500 mt-1">Historical ledger entries</p>
        </div>
      </div>

      {/* Movements Table */}
      <div className="bg-white rounded-2xl border border-slate-200/80 shadow-subtle overflow-hidden">
        <div className="p-4 border-b border-slate-100 flex items-center justify-between">
          <h3 className="text-base font-bold text-slate-900">Audit Trail: Movement History</h3>
          <span className="text-xs text-slate-500">Real documents in 'inventory_movements'</span>
        </div>

        {loading ? (
          <LoadingState message="Loading movement history from MongoDB..." />
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="bg-slate-50 text-slate-600 uppercase font-semibold border-b border-slate-200">
                <tr>
                  <th className="py-3 px-4">Date &amp; Time</th>
                  <th className="py-3 px-4">Product Name</th>
                  <th className="py-3 px-4">SKU</th>
                  <th className="py-3 px-4 text-center">Change Qty</th>
                  <th className="py-3 px-4">Reason / Audit Trail</th>
                  <th className="py-3 px-4 text-right">Related Order</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {movements.map((m) => {
                  const isPositive = m.change_quantity > 0;
                  return (
                    <tr key={m.id} className="hover:bg-slate-50/60 transition">
                      <td className="py-3 px-4 text-slate-600 whitespace-nowrap">
                        {m.created_at ? new Date(m.created_at).toLocaleString() : 'N/A'}
                      </td>
                      <td className="py-3 px-4 font-semibold text-slate-800">
                        {m.product_name || 'Product'}
                      </td>
                      <td className="py-3 px-4 font-mono text-slate-500">{m.sku || 'N/A'}</td>
                      <td className="py-3 px-4 text-center">
                        <span
                          className={`inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full font-bold text-xs ${
                            isPositive
                              ? 'bg-emerald-50 text-emerald-700 border border-emerald-200'
                              : 'bg-rose-50 text-rose-700 border border-rose-200'
                          }`}
                        >
                          {isPositive ? (
                            <ArrowUpRight className="w-3.5 h-3.5 text-emerald-600" />
                          ) : (
                            <ArrowDownRight className="w-3.5 h-3.5 text-rose-600" />
                          )}
                          {isPositive ? `+${m.change_quantity}` : m.change_quantity}
                        </span>
                      </td>
                      <td className="py-3 px-4 text-slate-700 font-medium">{m.reason}</td>
                      <td className="py-3 px-4 text-right font-mono text-slate-500">
                        {m.related_order_id ? `#${String(m.related_order_id).slice(-6).toUpperCase()}` : '—'}
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        )}

        {/* Pagination */}
        <div className="p-4 border-t border-slate-100 flex items-center justify-between text-xs text-slate-500">
          <p>
            Showing {(page - 1) * pageSize + 1} to {Math.min(page * pageSize, totalMovements)} of {totalMovements} records
          </p>
          <div className="flex items-center gap-2">
            <button
              onClick={() => setPage((p) => Math.max(1, p - 1))}
              disabled={page <= 1}
              className="flex items-center gap-1 px-3 py-1.5 bg-white border border-slate-200 rounded-xl hover:bg-slate-50 disabled:opacity-40 font-medium transition"
            >
              <ChevronLeft className="w-3.5 h-3.5" />
              <span>Prev</span>
            </button>
            <span className="px-2 font-semibold text-slate-800">
              Page {page} of {totalPages}
            </span>
            <button
              onClick={() => setPage((p) => Math.min(totalPages, p + 1))}
              disabled={page >= totalPages}
              className="flex items-center gap-1 px-3 py-1.5 bg-white border border-slate-200 rounded-xl hover:bg-slate-50 disabled:opacity-40 font-medium transition"
            >
              <span>Next</span>
              <ChevronRight className="w-3.5 h-3.5" />
            </button>
          </div>
        </div>
      </div>

      {/* Adjust Stock Modal */}
      {isAdjustModalOpen && (
        <Modal
          isOpen={isAdjustModalOpen}
          onClose={() => setIsAdjustModalOpen(false)}
          title="Manual Stock Adjustment"
          subtitle="Updates product stock and appends immutable movement audit record in MongoDB"
          maxWidth="md"
        >
          <form onSubmit={handleAdjustStock} className="space-y-4 text-xs">
            {actionError && (
              <div className="p-3 bg-rose-50 border border-rose-200 text-rose-700 rounded-xl font-medium">
                {actionError}
              </div>
            )}

            <div>
              <label className="block font-semibold text-slate-700 mb-1">Target Product SKU *</label>
              <select
                required
                value={adjustProductId}
                onChange={(e) => setAdjustProductId(e.target.value)}
                className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-xl outline-none focus:border-brand-500 font-medium"
              >
                {allProducts.map((p) => (
                  <option key={p.id} value={p.id}>
                    {p.name} ({p.sku}) — Current Stock: {p.stock_quantity}
                  </option>
                ))}
              </select>
            </div>

            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="block font-semibold text-slate-700 mb-1">Operation *</label>
                <div className="flex rounded-xl bg-slate-100 p-1">
                  <button
                    type="button"
                    onClick={() => {
                      setAdjustType('stock_in');
                      setAdjustReason('Supplier shipment arrival');
                    }}
                    className={`flex-1 py-1.5 rounded-lg font-semibold transition ${
                      adjustType === 'stock_in' ? 'bg-emerald-600 text-white shadow-xs' : 'text-slate-600'
                    }`}
                  >
                    + Stock In
                  </button>
                  <button
                    type="button"
                    onClick={() => {
                      setAdjustType('stock_out');
                      setAdjustReason('Warehouse inventory count correction');
                    }}
                    className={`flex-1 py-1.5 rounded-lg font-semibold transition ${
                      adjustType === 'stock_out' ? 'bg-rose-600 text-white shadow-xs' : 'text-slate-600'
                    }`}
                  >
                    - Stock Out
                  </button>
                </div>
              </div>

              <div>
                <label className="block font-semibold text-slate-700 mb-1">Quantity Units *</label>
                <input
                  type="number"
                  min="1"
                  required
                  value={adjustQty}
                  onChange={(e) => setAdjustQty(parseInt(e.target.value) || 1)}
                  className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-xl outline-none focus:border-brand-500 font-bold text-center"
                />
              </div>
            </div>

            <div>
              <label className="block font-semibold text-slate-700 mb-1">Audit Reason *</label>
              <input
                type="text"
                required
                value={adjustReason}
                onChange={(e) => setAdjustReason(e.target.value)}
                placeholder="e.g. Returned item restocked, damaged item write-off"
                className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-xl outline-none focus:border-brand-500"
              />
            </div>

            <div className="flex justify-end gap-2 pt-3 border-t border-slate-100">
              <button
                type="button"
                onClick={() => setIsAdjustModalOpen(false)}
                className="px-4 py-2 bg-slate-100 hover:bg-slate-200 text-slate-700 rounded-xl font-semibold"
              >
                Cancel
              </button>
              <button
                type="submit"
                className="px-5 py-2 bg-brand-600 hover:bg-brand-700 text-white rounded-xl font-semibold shadow-sm"
              >
                Apply Inventory Adjustment
              </button>
            </div>
          </form>
        </Modal>
      )}
    </div>
  );
};
