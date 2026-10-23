import React, { useEffect, useState } from 'react';
import {
  DollarSign,
  ShoppingBag,
  Users,
  Package,
  Clock,
  AlertTriangle,
  TrendingUp,
  ArrowRight,
  Eye,
  RefreshCw,
  Filter
} from 'lucide-react';
import {
  AreaChart,
  Area,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell
} from 'recharts';
import { apiClient } from '../api/client';
import { DashboardSummary, Order, Product } from '../types';
import { StatCard } from '../components/StatCard';
import { StatusBadge } from '../components/StatusBadge';
import { LoadingState } from '../components/EmptyState';
import { Modal } from '../components/Modal';

interface DashboardPageProps {
  onNavigate: (tab: string) => void;
}

const CATEGORY_COLORS = ['#3B82F6', '#10B981', '#F59E0B', '#8B5CF6', '#EC4899', '#06B6D4'];

export const DashboardPage: React.FC<DashboardPageProps> = ({ onNavigate }) => {
  const [data, setData] = useState<DashboardSummary | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedOrder, setSelectedOrder] = useState<Order | null>(null);

  const fetchDashboardData = async () => {
    try {
      setLoading(true);
      setError(null);
      const res = await apiClient.get('/dashboard/summary');
      if (res.data?.data) {
        setData(res.data.data);
      }
    } catch (err: any) {
      setError(err.message || 'Failed to fetch dashboard data');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDashboardData();
  }, []);

  if (loading && !data) {
    return <LoadingState message="Connecting to MongoDB & computing dashboard aggregations..." />;
  }

  if (error && !data) {
    return (
      <div className="p-8 text-center bg-white rounded-2xl border border-rose-200">
        <AlertTriangle className="w-10 h-10 text-rose-500 mx-auto mb-3" />
        <h3 className="text-base font-bold text-slate-800">MongoDB Query Error</h3>
        <p className="text-sm text-slate-600 mt-1 max-w-md mx-auto">{error}</p>
        <button
          onClick={fetchDashboardData}
          className="mt-4 px-4 py-2 bg-brand-600 text-white rounded-xl text-sm font-semibold hover:bg-brand-700 transition"
        >
          Retry Connection
        </button>
      </div>
    );
  }

  const metrics = data?.metrics;

  return (
    <div className="space-y-6">
      {/* Top Banner / Refresh header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 bg-white p-5 rounded-2xl border border-slate-200/80 shadow-subtle">
        <div>
          <h2 className="text-xl font-bold text-slate-900 tracking-tight">Executive Performance Hub</h2>
          <p className="text-xs text-slate-500 mt-0.5">
            Real-time NoSQL pipeline metrics computed across 100+ products, customers, and fulfillment orders.
          </p>
        </div>
        <div className="flex items-center gap-2.5">
          <button
            onClick={fetchDashboardData}
            disabled={loading}
            className="flex items-center gap-1.5 px-3 py-1.5 bg-slate-100 hover:bg-slate-200/80 text-slate-700 rounded-xl text-xs font-semibold transition"
          >
            <RefreshCw className={`w-3.5 h-3.5 ${loading ? 'animate-spin' : ''}`} />
            <span>Sync MongoDB</span>
          </button>
          <button
            onClick={() => onNavigate('concepts')}
            className="flex items-center gap-1.5 px-3.5 py-1.5 bg-brand-600 hover:bg-brand-700 text-white rounded-xl text-xs font-semibold shadow-sm transition"
          >
            <span>Inspect Aggregation Code</span>
            <ArrowRight className="w-3.5 h-3.5" />
          </button>
        </div>
      </div>

      {/* KPI Cards Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-6 gap-4">
        <StatCard
          title="Total Revenue"
          value={`$${(metrics?.total_revenue || 0).toLocaleString('en-US', { minimumFractionDigits: 2 })}`}
          subtitle="All confirmed orders"
          icon={DollarSign}
          color="emerald"
        />
        <StatCard
          title="Total Orders"
          value={metrics?.total_orders || 0}
          subtitle={`AOV: $${metrics?.average_order_value || 0}`}
          icon={ShoppingBag}
          color="blue"
        />
        <StatCard
          title="Customers"
          value={metrics?.total_customers || 0}
          subtitle="Registered accounts"
          icon={Users}
          color="indigo"
        />
        <StatCard
          title="Live Catalogue"
          value={metrics?.total_products || 0}
          subtitle="Active SKU units"
          icon={Package}
          color="purple"
        />
        <StatCard
          title="Pending Orders"
          value={metrics?.pending_orders || 0}
          subtitle="Requires fulfillment"
          icon={Clock}
          color="amber"
        />
        <StatCard
          title="Low Stock"
          value={metrics?.low_stock_products_count || 0}
          subtitle="<= 10 units left"
          icon={AlertTriangle}
          color="rose"
        />
      </div>

      {/* Charts Section: Monthly Trend & Category Breakdown */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Monthly Revenue Trend */}
        <div className="lg:col-span-2 bg-white p-5 rounded-2xl border border-slate-200/80 shadow-subtle">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h3 className="text-base font-bold text-slate-900">Monthly Revenue Pipeline</h3>
              <p className="text-xs text-slate-500">Aggregated with $dateToString and $group stages</p>
            </div>
            <span className="text-xs font-semibold px-2.5 py-1 rounded-full bg-brand-50 text-brand-700 border border-brand-200">
              6 Month Time Series
            </span>
          </div>

          <div className="h-64 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={data?.monthly_trends || []} margin={{ top: 10, right: 10, left: 0, bottom: 0 }}>
                <defs>
                  <linearGradient id="colorRev" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#3B82F6" stopOpacity={0.3} />
                    <stop offset="95%" stopColor="#3B82F6" stopOpacity={0} />
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#E2E8F0" />
                <XAxis dataKey="month" stroke="#94A3B8" fontSize={11} tickLine={false} />
                <YAxis
                  stroke="#94A3B8"
                  fontSize={11}
                  tickLine={false}
                  axisLine={false}
                  tickFormatter={(val) => `$${val >= 1000 ? `${(val / 1000).toFixed(0)}k` : val}`}
                />
                <Tooltip
                  formatter={(val: any) => [`$${Number(val).toLocaleString()}`, 'Revenue']}
                  contentStyle={{ backgroundColor: '#0B132B', color: '#fff', borderRadius: '10px', fontSize: '12px' }}
                />
                <Area type="monotone" dataKey="revenue" stroke="#2563EB" strokeWidth={2.5} fillOpacity={1} fill="url(#colorRev)" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Category Sales Breakdown */}
        <div className="bg-white p-5 rounded-2xl border border-slate-200/80 shadow-subtle flex flex-col justify-between">
          <div>
            <h3 className="text-base font-bold text-slate-900">Sales by Category</h3>
            <p className="text-xs text-slate-500">Unwound embedded order line-totals</p>

            <div className="h-44 w-full mt-2">
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={data?.category_sales || []}
                    cx="50%"
                    cy="50%"
                    innerRadius={45}
                    outerRadius={65}
                    paddingAngle={3}
                    dataKey="total_revenue"
                  >
                    {(data?.category_sales || []).map((_, index) => (
                      <Cell key={`cell-${index}`} fill={CATEGORY_COLORS[index % CATEGORY_COLORS.length]} />
                    ))}
                  </Pie>
                  <Tooltip
                    formatter={(val: any) => [`$${Number(val).toLocaleString()}`, 'Revenue']}
                    contentStyle={{ backgroundColor: '#0B132B', color: '#fff', borderRadius: '8px', fontSize: '11px' }}
                  />
                </PieChart>
              </ResponsiveContainer>
            </div>
          </div>

          <div className="space-y-1.5 mt-2 max-h-32 overflow-y-auto pr-1">
            {(data?.category_sales || []).map((cat, idx) => (
              <div key={cat.category} className="flex items-center justify-between text-xs py-1 border-b border-slate-100 last:border-0">
                <div className="flex items-center gap-2">
                  <span
                    className="w-2.5 h-2.5 rounded-full"
                    style={{ backgroundColor: CATEGORY_COLORS[idx % CATEGORY_COLORS.length] }}
                  />
                  <span className="font-medium text-slate-700 truncate max-w-[120px]">{cat.category}</span>
                </div>
                <span className="font-bold text-slate-900">${cat.total_revenue.toLocaleString()}</span>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Two-Column Section: Top Selling Products & Low Stock Alerts */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Top-Selling Products */}
        <div className="lg:col-span-2 bg-white p-5 rounded-2xl border border-slate-200/80 shadow-subtle">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h3 className="text-base font-bold text-slate-900">Top-Selling Products</h3>
              <p className="text-xs text-slate-500">Calculated via $unwind and $group by units sold</p>
            </div>
            <button
              onClick={() => onNavigate('products')}
              className="text-xs font-semibold text-brand-600 hover:text-brand-700 flex items-center gap-1"
            >
              <span>Catalogue</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </button>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="bg-slate-50 text-slate-600 uppercase font-semibold">
                <tr>
                  <th className="py-2.5 px-3 rounded-l-lg">Product</th>
                  <th className="py-2.5 px-3">SKU</th>
                  <th className="py-2.5 px-3">Category</th>
                  <th className="py-2.5 px-3 text-right">Units Sold</th>
                  <th className="py-2.5 px-3 text-right rounded-r-lg">Gross Revenue</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {(data?.top_products || []).map((prod) => (
                  <tr key={prod.product_id} className="hover:bg-slate-50/60 transition">
                    <td className="py-2.5 px-3 font-semibold text-slate-800">{prod.name}</td>
                    <td className="py-2.5 px-3 font-mono text-slate-500">{prod.sku}</td>
                    <td className="py-2.5 px-3 text-slate-600">{prod.category}</td>
                    <td className="py-2.5 px-3 text-right font-semibold text-slate-700">{prod.units_sold}</td>
                    <td className="py-2.5 px-3 text-right font-bold text-emerald-600">
                      ${prod.total_revenue.toLocaleString('en-US', { minimumFractionDigits: 2 })}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Low-Stock Alerts */}
        <div className="bg-white p-5 rounded-2xl border border-slate-200/80 shadow-subtle flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between mb-3">
              <div className="flex items-center gap-2">
                <AlertTriangle className="w-4 h-4 text-amber-500" />
                <h3 className="text-base font-bold text-slate-900">Low-Stock Watchlist</h3>
              </div>
              <button
                onClick={() => onNavigate('inventory')}
                className="text-xs font-semibold text-brand-600 hover:text-brand-700"
              >
                Inventory
              </button>
            </div>
            <p className="text-xs text-slate-500 mb-3">Items requiring warehouse reorder</p>

            <div className="space-y-2.5">
              {(data?.low_stock_alerts || []).slice(0, 5).map((item) => (
                <div
                  key={item.id}
                  className="p-2.5 rounded-xl border border-amber-100 bg-amber-50/50 flex items-center justify-between text-xs"
                >
                  <div>
                    <p className="font-semibold text-slate-800 line-clamp-1">{item.name}</p>
                    <p className="text-[10px] text-slate-500 font-mono">{item.sku}</p>
                  </div>
                  <div className="text-right">
                    <span className="inline-block px-2 py-0.5 rounded-full text-[10px] font-bold bg-amber-200 text-amber-800">
                      {item.stock_quantity} left
                    </span>
                    <p className="text-[10px] text-slate-500 mt-0.5">${item.price}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>

          <button
            onClick={() => onNavigate('inventory')}
            className="w-full mt-4 py-2 text-xs font-semibold text-center text-slate-700 bg-slate-100 hover:bg-slate-200 rounded-xl transition"
          >
            Manage All Inventory Movements
          </button>
        </div>
      </div>

      {/* Recent Orders Table */}
      <div className="bg-white p-5 rounded-2xl border border-slate-200/80 shadow-subtle">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h3 className="text-base font-bold text-slate-900">Recent Customer Orders</h3>
            <p className="text-xs text-slate-500">Real orders fetched from MongoDB 'orders' collection</p>
          </div>
          <button
            onClick={() => onNavigate('orders')}
            className="text-xs font-semibold text-brand-600 hover:text-brand-700 flex items-center gap-1"
          >
            <span>View All Orders</span>
            <ArrowRight className="w-3.5 h-3.5" />
          </button>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead className="bg-slate-50 text-slate-600 uppercase font-semibold">
              <tr>
                <th className="py-2.5 px-3 rounded-l-lg">Order ID</th>
                <th className="py-2.5 px-3">Customer</th>
                <th className="py-2.5 px-3">Date</th>
                <th className="py-2.5 px-3">Items</th>
                <th className="py-2.5 px-3">Status</th>
                <th className="py-2.5 px-3 text-right">Subtotal</th>
                <th className="py-2.5 px-3 text-center rounded-r-lg">Action</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {(data?.recent_orders || []).map((order) => (
                <tr key={order.id} className="hover:bg-slate-50/60 transition">
                  <td className="py-3 px-3 font-mono font-medium text-brand-600">
                    #{order.id.slice(-6).toUpperCase()}
                  </td>
                  <td className="py-3 px-3">
                    <p className="font-semibold text-slate-800">{order.customer_name || 'Guest'}</p>
                    <p className="text-[10px] text-slate-400">{order.customer_email}</p>
                  </td>
                  <td className="py-3 px-3 text-slate-600">
                    {order.created_at ? new Date(order.created_at).toLocaleDateString() : 'N/A'}
                  </td>
                  <td className="py-3 px-3 text-slate-600">
                    {order.items.length} {order.items.length === 1 ? 'item' : 'items'}
                  </td>
                  <td className="py-3 px-3">
                    <StatusBadge status={order.status} />
                  </td>
                  <td className="py-3 px-3 text-right font-bold text-slate-900">
                    ${order.subtotal.toFixed(2)}
                  </td>
                  <td className="py-3 px-3 text-center">
                    <button
                      onClick={() => setSelectedOrder(order)}
                      className="p-1.5 text-slate-500 hover:text-brand-600 hover:bg-brand-50 rounded-lg transition"
                      title="Inspect Embedded Snapshot"
                    >
                      <Eye className="w-4 h-4" />
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Order Detail Modal */}
      {selectedOrder && (
        <Modal
          isOpen={!!selectedOrder}
          onClose={() => setSelectedOrder(null)}
          title={`Order #${selectedOrder.id.slice(-6).toUpperCase()} — Embedded Snapshot`}
          subtitle={`Placed on ${selectedOrder.created_at ? new Date(selectedOrder.created_at).toLocaleString() : ''}`}
          maxWidth="2xl"
        >
          <div className="space-y-4">
            <div className="flex items-center justify-between p-3 bg-slate-50 rounded-xl border border-slate-100">
              <div>
                <p className="text-xs text-slate-500">Customer ObjectId Reference</p>
                <p className="text-xs font-mono font-bold text-slate-800">{selectedOrder.customer_id}</p>
                <p className="text-xs text-slate-600 mt-0.5">{selectedOrder.customer_name} ({selectedOrder.customer_email})</p>
              </div>
              <StatusBadge status={selectedOrder.status} />
            </div>

            <div>
              <h4 className="text-xs font-bold uppercase tracking-wider text-slate-500 mb-2">
                Embedded Items Snapshot
              </h4>
              <div className="border border-slate-200 rounded-xl overflow-hidden text-xs">
                <table className="w-full text-left">
                  <thead className="bg-slate-50 text-slate-600 font-semibold border-b border-slate-200">
                    <tr>
                      <th className="p-2.5">Item Name</th>
                      <th className="p-2.5">SKU</th>
                      <th className="p-2.5 text-right">Price</th>
                      <th className="p-2.5 text-right">Qty</th>
                      <th className="p-2.5 text-right">Total</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-100">
                    {selectedOrder.items.map((item, idx) => (
                      <tr key={idx}>
                        <td className="p-2.5 font-medium text-slate-800">{item.name}</td>
                        <td className="p-2.5 font-mono text-slate-500">{item.sku}</td>
                        <td className="p-2.5 text-right">${item.unit_price.toFixed(2)}</td>
                        <td className="p-2.5 text-right font-semibold">{item.quantity}</td>
                        <td className="p-2.5 text-right font-bold text-slate-900">${item.line_total.toFixed(2)}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>

            <div className="flex justify-between items-center pt-2 border-t border-slate-100">
              <div className="text-xs text-slate-500">
                <p className="font-semibold text-slate-700">Shipping Address (Embedded):</p>
                <p>{selectedOrder.shipping_address.street}, {selectedOrder.shipping_address.city}, {selectedOrder.shipping_address.state} {selectedOrder.shipping_address.postal_code}</p>
              </div>
              <div className="text-right">
                <p className="text-xs text-slate-500">Order Subtotal</p>
                <p className="text-xl font-bold text-slate-900">${selectedOrder.subtotal.toFixed(2)}</p>
              </div>
            </div>
          </div>
        </Modal>
      )}
    </div>
  );
};
