import React, { useEffect, useState } from 'react';
import {
  ShoppingBag,
  Search,
  Plus,
  Eye,
  Calendar,
  DollarSign,
  ChevronLeft,
  ChevronRight,
  CheckCircle,
  Truck,
  RotateCcw,
  AlertCircle,
  X,
  Check
} from 'lucide-react';
import { apiClient } from '../api/client';
import { Customer, Order, OrderStatus, PaginatedResult, Product } from '../types';
import { StatusBadge } from '../components/StatusBadge';
import { Modal } from '../components/Modal';
import { EmptyState, LoadingState } from '../components/EmptyState';

export const OrdersPage: React.FC = () => {
  const [orders, setOrders] = useState<Order[]>([]);
  const [total, setTotal] = useState<number>(0);
  const [page, setPage] = useState<number>(1);
  const [pageSize] = useState<number>(15);
  const [totalPages, setTotalPages] = useState<number>(1);
  const [loading, setLoading] = useState<boolean>(true);

  // Filters
  const [search, setSearch] = useState<string>('');
  const [statusFilter, setStatusFilter] = useState<string>('');

  // Modals & Inspection
  const [selectedOrder, setSelectedOrder] = useState<Order | null>(null);
  const [isCreateModalOpen, setIsCreateModalOpen] = useState<boolean>(false);
  const [actionSuccess, setActionSuccess] = useState<string | null>(null);
  const [actionError, setActionError] = useState<string | null>(null);

  // New Order Form state
  const [customers, setCustomers] = useState<Customer[]>([]);
  const [availableProducts, setAvailableProducts] = useState<Product[]>([]);
  const [newOrderCustomerId, setNewOrderCustomerId] = useState<string>('');
  const [newOrderItems, setNewOrderItems] = useState<{ productId: string; quantity: number }[]>([]);
  const [shippingStreet, setShippingStreet] = useState<string>('500 Tech Blvd');
  const [shippingCity, setShippingCity] = useState<string>('San Francisco');
  const [shippingZip, setShippingZip] = useState<string>('94105');

  const fetchOrders = async () => {
    try {
      setLoading(true);
      const params: any = { page, page_size: pageSize };
      if (search.trim()) params.search = search.trim();
      if (statusFilter) params.status = statusFilter;

      const res = await apiClient.get('/orders', { params });
      const data: PaginatedResult<Order> = res.data;
      setOrders(data.items || []);
      setTotal(data.total || 0);
      setTotalPages(data.total_pages || 1);
    } catch (e) {
      console.error('Error fetching orders:', e);
    } finally {
      setLoading(false);
    }
  };

  const fetchCreateDependencies = async () => {
    try {
      const [cRes, pRes] = await Promise.all([
        apiClient.get('/customers?page=1&page_size=50'),
        apiClient.get('/products?page=1&page_size=50&stock_status=in_stock'),
      ]);
      const custs = cRes.data.items || [];
      const prods = pRes.data.items || [];
      setCustomers(custs);
      setAvailableProducts(prods);
      if (custs.length > 0) setNewOrderCustomerId(custs[0].id);
      if (prods.length > 0) setNewOrderItems([{ productId: prods[0].id, quantity: 1 }]);
    } catch (e) {
      console.error('Error loading order form dependencies:', e);
    }
  };

  useEffect(() => {
    fetchOrders();
  }, [page, search, statusFilter]);

  const handleStatusChange = async (orderId: string, newStatus: OrderStatus) => {
    setActionError(null);
    try {
      await apiClient.patch(`/orders/${orderId}/status`, {
        status: newStatus,
        reason: `Status transitioned via Admin Dashboard to ${newStatus}`,
      });
      setActionSuccess(`Order status transitioned to '${newStatus}'. If cancelled, stock was safely restored in MongoDB.`);
      fetchOrders();
      if (selectedOrder && selectedOrder.id === orderId) {
        setSelectedOrder({ ...selectedOrder, status: newStatus });
      }
      setTimeout(() => setActionSuccess(null), 5000);
    } catch (err: any) {
      setActionError(err.message || 'Status transition rejected');
      setTimeout(() => setActionError(null), 5000);
    }
  };

  const handleCreateOrder = async (e: React.FormEvent) => {
    e.preventDefault();
    setActionError(null);

    if (newOrderItems.length === 0) {
      setActionError('Please add at least one product item');
      return;
    }

    const payload = {
      customer_id: newOrderCustomerId,
      items: newOrderItems.map((item) => ({
        product_id: item.productId,
        quantity: Number(item.quantity),
      })),
      shipping_address: {
        street: shippingStreet,
        city: shippingCity,
        state: 'CA',
        postal_code: shippingZip,
        country: 'USA',
      },
    };

    try {
      const res = await apiClient.post('/orders', payload);
      setIsCreateModalOpen(false);
      setActionSuccess(`Order #${res.data?.data?.id?.slice(-6).toUpperCase()} created successfully! Stock decremented & inventory movement logged.`);
      fetchOrders();
      setTimeout(() => setActionSuccess(null), 5000);
    } catch (err: any) {
      setActionError(err.message || 'Failed to place order');
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 bg-white p-5 rounded-2xl border border-slate-200/80 shadow-subtle">
        <div>
          <h2 className="text-xl font-bold text-slate-900 tracking-tight">Order Management &amp; Fulfillment</h2>
          <p className="text-xs text-slate-500 mt-0.5">
            Embedded snapshots, atomic inventory decrements, and transactional status workflows.
          </p>
        </div>
        <button
          onClick={() => {
            fetchCreateDependencies();
            setIsCreateModalOpen(true);
          }}
          className="flex items-center gap-1.5 px-4 py-2 bg-brand-600 hover:bg-brand-700 text-white rounded-xl text-xs font-semibold shadow-sm transition"
        >
          <Plus className="w-4 h-4" />
          <span>Create New Order</span>
        </button>
      </div>

      {actionSuccess && (
        <div className="p-3 bg-emerald-50 border border-emerald-200 text-emerald-800 rounded-xl text-xs flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Check className="w-4 h-4 text-emerald-600 shrink-0" />
            <span className="font-medium">{actionSuccess}</span>
          </div>
          <button onClick={() => setActionSuccess(null)}>
            <X className="w-4 h-4 text-emerald-600" />
          </button>
        </div>
      )}

      {actionError && (
        <div className="p-3 bg-rose-50 border border-rose-200 text-rose-800 rounded-xl text-xs flex items-center justify-between">
          <div className="flex items-center gap-2">
            <AlertCircle className="w-4 h-4 text-rose-600 shrink-0" />
            <span className="font-medium">{actionError}</span>
          </div>
          <button onClick={() => setActionError(null)}>
            <X className="w-4 h-4 text-rose-600" />
          </button>
        </div>
      )}

      {/* Filters Bar */}
      <div className="bg-white p-4 rounded-2xl border border-slate-200/80 shadow-subtle flex flex-wrap items-center justify-between gap-3 text-xs">
        <div className="relative flex-1 min-w-[200px] max-w-sm">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
          <input
            type="text"
            placeholder="Search order ID, item name, SKU..."
            value={search}
            onChange={(e) => {
              setSearch(e.target.value);
              setPage(1);
            }}
            className="w-full pl-9 pr-3 py-1.5 bg-slate-50 border border-slate-200 rounded-xl outline-none focus:border-brand-500"
          />
        </div>

        <div className="flex items-center gap-2">
          <select
            value={statusFilter}
            onChange={(e) => {
              setStatusFilter(e.target.value);
              setPage(1);
            }}
            className="px-3 py-1.5 bg-slate-50 border border-slate-200 rounded-xl text-slate-700 font-medium outline-none focus:border-brand-500"
          >
            <option value="">All Statuses</option>
            <option value="pending">Pending</option>
            <option value="confirmed">Confirmed</option>
            <option value="shipped">Shipped</option>
            <option value="delivered">Delivered</option>
            <option value="cancelled">Cancelled</option>
          </select>
        </div>
      </div>

      {/* Orders Table */}
      {loading ? (
        <LoadingState message="Fetching orders from MongoDB..." />
      ) : orders.length === 0 ? (
        <EmptyState
          icon={ShoppingBag}
          title="No Orders Found"
          description="No orders match your filter criteria. Clear filters or create an order."
          actionText="Create Order"
          onAction={() => {
            fetchCreateDependencies();
            setIsCreateModalOpen(true);
          }}
        />
      ) : (
        <div className="bg-white rounded-2xl border border-slate-200/80 shadow-subtle overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="bg-slate-50 text-slate-600 uppercase font-semibold border-b border-slate-200">
                <tr>
                  <th className="py-3 px-4">Order ID</th>
                  <th className="py-3 px-4">Customer</th>
                  <th className="py-3 px-4">Date Placed</th>
                  <th className="py-3 px-4">Items Preview</th>
                  <th className="py-3 px-4">Status</th>
                  <th className="py-3 px-4 text-right">Subtotal</th>
                  <th className="py-3 px-4 text-center">Fulfillment Action</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {orders.map((o) => (
                  <tr key={o.id} className="hover:bg-slate-50/60 transition">
                    <td className="py-3 px-4">
                      <div className="flex items-center gap-1.5">
                        <span className="font-mono font-bold text-brand-600">
                          #{o.id.slice(-6).toUpperCase()}
                        </span>
                        {o.source === 'olist_real' ? (
                          <span className="px-1.5 py-0.5 bg-blue-50 text-blue-700 text-[9px] font-semibold rounded border border-blue-200" title={`Olist Order: ${o.external_id || o.id}`}>
                            Olist
                          </span>
                        ) : (
                          <span className="px-1.5 py-0.5 bg-emerald-50 text-emerald-700 text-[9px] font-semibold rounded border border-emerald-200">
                            Demo
                          </span>
                        )}
                      </div>
                    </td>
                    <td className="py-3 px-4">
                      <p className="font-semibold text-slate-800">{o.customer_name || 'Customer'}</p>
                      <p className="text-[10px] text-slate-400 font-mono">{o.customer_id.slice(-6)}</p>
                    </td>
                    <td className="py-3 px-4 text-slate-600">
                      {o.created_at ? new Date(o.created_at).toLocaleDateString() : 'N/A'}
                    </td>
                    <td className="py-3 px-4 max-w-[200px]">
                      <p className="truncate text-slate-700 font-medium">
                        {o.items.map((i) => `${i.name} (x${i.quantity})`).join(', ')}
                      </p>
                      <p className="text-[10px] text-slate-400">{o.items.length} items total</p>
                    </td>
                    <td className="py-3 px-4">
                      <StatusBadge status={o.status} />
                    </td>
                    <td className="py-3 px-4 text-right font-bold text-slate-900">
                      ${o.subtotal.toFixed(2)}
                    </td>
                    <td className="py-3 px-4 text-center">
                      <div className="flex items-center justify-center gap-1.5">
                        <button
                          onClick={() => setSelectedOrder(o)}
                          className="px-2 py-1 text-slate-600 hover:text-brand-600 hover:bg-slate-100 rounded-lg transition font-medium flex items-center gap-1"
                        >
                          <Eye className="w-3.5 h-3.5" />
                          <span>View</span>
                        </button>

                        {/* Status Transition Quick Actions (Isolated for Demo Orders Only) */}
                        {o.source === 'olist_real' ? (
                          <span className="text-[10px] text-slate-400 italic">Immutable</span>
                        ) : (
                          <>
                            {o.status === 'pending' && (
                              <button
                                onClick={() => handleStatusChange(o.id, 'confirmed')}
                                className="px-2 py-1 bg-indigo-50 text-indigo-700 hover:bg-indigo-100 rounded-lg font-medium transition"
                              >
                                Confirm
                              </button>
                            )}
                            {o.status === 'confirmed' && (
                              <button
                                onClick={() => handleStatusChange(o.id, 'shipped')}
                                className="px-2 py-1 bg-blue-50 text-blue-700 hover:bg-blue-100 rounded-lg font-medium transition"
                              >
                                Ship
                              </button>
                            )}
                            {o.status === 'shipped' && (
                              <button
                                onClick={() => handleStatusChange(o.id, 'delivered')}
                                className="px-2 py-1 bg-emerald-50 text-emerald-700 hover:bg-emerald-100 rounded-lg font-medium transition"
                              >
                                Deliver
                              </button>
                            )}
                            {(o.status === 'pending' || o.status === 'confirmed') && (
                              <button
                                onClick={() => handleStatusChange(o.id, 'cancelled')}
                                className="px-2 py-1 bg-rose-50 text-rose-700 hover:bg-rose-100 rounded-lg font-medium transition"
                                title="Cancels demo order and restores stock"
                              >
                                Cancel
                              </button>
                            )}
                          </>
                        )}
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Pagination */}
      <div className="flex items-center justify-between text-xs text-slate-500 pt-2">
        <p>
          Showing {(page - 1) * pageSize + 1} to {Math.min(page * pageSize, total)} of {total} orders
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

      {/* Order Detail Modal */}
      {selectedOrder && (
        <Modal
          isOpen={!!selectedOrder}
          onClose={() => setSelectedOrder(null)}
          title={`Order #${selectedOrder.id.slice(-6).toUpperCase()}`}
          subtitle={`MongoDB Document ID: ${selectedOrder.id}`}
          maxWidth="2xl"
        >
          <div className="space-y-4 text-xs">
            {/* Status and Transition bar */}
            <div className="flex items-center justify-between p-3.5 bg-slate-50 rounded-xl border border-slate-200">
              <div className="flex items-center gap-2">
                <span className="font-semibold text-slate-700">Status:</span>
                <StatusBadge status={selectedOrder.status} />
              </div>
              <div className="flex items-center gap-1.5">
                {selectedOrder.status === 'pending' && (
                  <button
                    onClick={() => handleStatusChange(selectedOrder.id, 'confirmed')}
                    className="px-2.5 py-1 bg-indigo-600 text-white rounded-lg font-semibold hover:bg-indigo-700 transition"
                  >
                    Confirm Order
                  </button>
                )}
                {selectedOrder.status === 'confirmed' && (
                  <button
                    onClick={() => handleStatusChange(selectedOrder.id, 'shipped')}
                    className="px-2.5 py-1 bg-blue-600 text-white rounded-lg font-semibold hover:bg-blue-700 transition"
                  >
                    Mark Shipped
                  </button>
                )}
                {selectedOrder.status === 'shipped' && (
                  <button
                    onClick={() => handleStatusChange(selectedOrder.id, 'delivered')}
                    className="px-2.5 py-1 bg-emerald-600 text-white rounded-lg font-semibold hover:bg-emerald-700 transition"
                  >
                    Mark Delivered
                  </button>
                )}
                {(selectedOrder.status === 'pending' || selectedOrder.status === 'confirmed') && (
                  <button
                    onClick={() => handleStatusChange(selectedOrder.id, 'cancelled')}
                    className="px-2.5 py-1 bg-rose-600 text-white rounded-lg font-semibold hover:bg-rose-700 transition"
                  >
                    Cancel &amp; Restore Stock
                  </button>
                )}
              </div>
            </div>

            {/* Embedded Items Table */}
            <div>
              <h4 className="font-bold text-slate-900 uppercase text-[11px] tracking-wider mb-2">
                Embedded Items (Snapshot In MongoDB)
              </h4>
              <div className="border border-slate-200 rounded-xl overflow-hidden">
                <table className="w-full text-left">
                  <thead className="bg-slate-50 text-slate-600 font-semibold border-b border-slate-200">
                    <tr>
                      <th className="p-2.5">Item Name</th>
                      <th className="p-2.5">SKU</th>
                      <th className="p-2.5 text-right">Price Snapshot</th>
                      <th className="p-2.5 text-right">Qty</th>
                      <th className="p-2.5 text-right">Line Total</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-100">
                    {selectedOrder.items.map((i, idx) => (
                      <tr key={idx}>
                        <td className="p-2.5 font-medium text-slate-800">{i.name}</td>
                        <td className="p-2.5 font-mono text-slate-500">{i.sku}</td>
                        <td className="p-2.5 text-right font-medium">${i.unit_price.toFixed(2)}</td>
                        <td className="p-2.5 text-right font-semibold">{i.quantity}</td>
                        <td className="p-2.5 text-right font-bold text-slate-900">${i.line_total.toFixed(2)}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>

            {/* Customer Reference & Shipping */}
            <div className="grid grid-cols-2 gap-3 pt-2">
              <div className="p-3 bg-slate-50 rounded-xl border border-slate-100">
                <p className="font-bold text-slate-800 mb-1">Referenced Customer Document</p>
                <p className="text-slate-600 font-mono text-[11px]">ID: {selectedOrder.customer_id}</p>
                <p className="text-slate-800 font-semibold mt-1">{selectedOrder.customer_name}</p>
                <p className="text-slate-500">{selectedOrder.customer_email}</p>
              </div>

              <div className="p-3 bg-slate-50 rounded-xl border border-slate-100">
                <p className="font-bold text-slate-800 mb-1">Embedded Shipping Address</p>
                <p className="text-slate-700">{selectedOrder.shipping_address.street}</p>
                <p className="text-slate-700">
                  {selectedOrder.shipping_address.city}, {selectedOrder.shipping_address.state}{' '}
                  {selectedOrder.shipping_address.postal_code}
                </p>
                <p className="text-slate-500">{selectedOrder.shipping_address.country}</p>
              </div>
            </div>

            {/* Subtotal Footer */}
            <div className="flex justify-between items-center pt-3 border-t border-slate-100">
              <p className="text-slate-500 text-[11px]">
                Server-side verified total: sum of item line totals.
              </p>
              <div className="text-right">
                <p className="text-xs text-slate-500">Order Subtotal</p>
                <p className="text-xl font-bold text-slate-900">${selectedOrder.subtotal.toFixed(2)}</p>
              </div>
            </div>
          </div>
        </Modal>
      )}

      {/* Create Order Modal */}
      {isCreateModalOpen && (
        <Modal
          isOpen={isCreateModalOpen}
          onClose={() => setIsCreateModalOpen(false)}
          title="Place New Order"
          subtitle="Validates stock, takes item snapshots, and updates MongoDB atomically"
          maxWidth="xl"
        >
          <form onSubmit={handleCreateOrder} className="space-y-4 text-xs">
            {actionError && (
              <div className="p-3 bg-rose-50 border border-rose-200 text-rose-700 rounded-xl font-medium">
                {actionError}
              </div>
            )}

            <div>
              <label className="block font-semibold text-slate-700 mb-1">Select Customer *</label>
              <select
                required
                value={newOrderCustomerId}
                onChange={(e) => setNewOrderCustomerId(e.target.value)}
                className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-xl outline-none focus:border-brand-500 font-medium"
              >
                {customers.map((c) => (
                  <option key={c.id} value={c.id}>
                    {c.name} ({c.email})
                  </option>
                ))}
              </select>
            </div>

            {/* Order Items */}
            <div>
              <div className="flex items-center justify-between mb-1">
                <label className="font-semibold text-slate-700">Order Line Items *</label>
                <button
                  type="button"
                  onClick={() => {
                    if (availableProducts.length > 0) {
                      setNewOrderItems([...newOrderItems, { productId: availableProducts[0].id, quantity: 1 }]);
                    }
                  }}
                  className="text-brand-600 font-semibold hover:text-brand-700"
                >
                  + Add Another Product
                </button>
              </div>

              <div className="space-y-2">
                {newOrderItems.map((item, index) => (
                  <div key={index} className="flex items-center gap-2">
                    <select
                      value={item.productId}
                      onChange={(e) => {
                        const next = [...newOrderItems];
                        next[index].productId = e.target.value;
                        setNewOrderItems(next);
                      }}
                      className="flex-1 px-3 py-2 bg-slate-50 border border-slate-200 rounded-xl outline-none focus:border-brand-500 font-medium"
                    >
                      {availableProducts.map((p) => (
                        <option key={p.id} value={p.id}>
                          {p.name} — ${p.price} ({p.stock_quantity} available)
                        </option>
                      ))}
                    </select>

                    <input
                      type="number"
                      min="1"
                      required
                      value={item.quantity}
                      onChange={(e) => {
                        const next = [...newOrderItems];
                        next[index].quantity = parseInt(e.target.value) || 1;
                        setNewOrderItems(next);
                      }}
                      className="w-20 px-3 py-2 bg-slate-50 border border-slate-200 rounded-xl outline-none focus:border-brand-500 text-center font-bold"
                    />

                    {newOrderItems.length > 1 && (
                      <button
                        type="button"
                        onClick={() => setNewOrderItems(newOrderItems.filter((_, idx) => idx !== index))}
                        className="p-2 text-rose-500 hover:bg-rose-50 rounded-xl"
                      >
                        <X className="w-4 h-4" />
                      </button>
                    )}
                  </div>
                ))}
              </div>
            </div>

            {/* Shipping Address Inputs */}
            <div>
              <label className="block font-semibold text-slate-700 mb-1">Shipping Street Address *</label>
              <input
                type="text"
                required
                value={shippingStreet}
                onChange={(e) => setShippingStreet(e.target.value)}
                className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-xl outline-none focus:border-brand-500"
              />
            </div>

            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="block font-semibold text-slate-700 mb-1">City *</label>
                <input
                  type="text"
                  required
                  value={shippingCity}
                  onChange={(e) => setShippingCity(e.target.value)}
                  className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-xl outline-none focus:border-brand-500"
                />
              </div>
              <div>
                <label className="block font-semibold text-slate-700 mb-1">Postal Code *</label>
                <input
                  type="text"
                  required
                  value={shippingZip}
                  onChange={(e) => setShippingZip(e.target.value)}
                  className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-xl outline-none focus:border-brand-500"
                />
              </div>
            </div>

            <div className="flex justify-end gap-2 pt-3 border-t border-slate-100">
              <button
                type="button"
                onClick={() => setIsCreateModalOpen(false)}
                className="px-4 py-2 bg-slate-100 hover:bg-slate-200 text-slate-700 rounded-xl font-semibold"
              >
                Cancel
              </button>
              <button
                type="submit"
                className="px-5 py-2 bg-brand-600 hover:bg-brand-700 text-white rounded-xl font-semibold shadow-sm"
              >
                Submit Order to MongoDB
              </button>
            </div>
          </form>
        </Modal>
      )}
    </div>
  );
};
