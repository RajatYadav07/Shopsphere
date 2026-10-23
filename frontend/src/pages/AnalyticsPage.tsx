import React, { useEffect, useState } from 'react';
import {
  BarChart3,
  TrendingUp,
  Download,
  Users,
  ShoppingBag,
  DollarSign,
  PieChart as PieIcon,
  Layers,
  Star,
  RefreshCw,
  FileSpreadsheet
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
  Cell,
  Legend
} from 'recharts';
import { apiClient } from '../api/client';
import { LoadingState } from '../components/EmptyState';
import { StatCard } from '../components/StatCard';

const PALETTE = ['#3B82F6', '#10B981', '#F59E0B', '#8B5CF6', '#EC4899', '#06B6D4'];

export const AnalyticsPage: React.FC = () => {
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [exporting, setExporting] = useState<boolean>(false);

  const fetchAnalytics = async () => {
    try {
      setLoading(true);
      const res = await apiClient.get('/analytics/overview');
      setData(res.data?.data || null);
    } catch (e) {
      console.error('Error fetching analytics:', e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchAnalytics();
  }, []);

  const handleExportCSV = async (type: string) => {
    try {
      setExporting(true);
      const res = await apiClient.get(`/analytics/export-csv?report_type=${type}`, {
        responseType: 'blob',
      });
      const url = window.URL.createObjectURL(new Blob([res.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `shopsphere_${type}_report.csv`);
      document.body.appendChild(link);
      link.click();
      link.remove();
    } catch (e) {
      alert('Error downloading CSV report');
    } finally {
      setExporting(false);
    }
  };

  if (loading && !data) {
    return <LoadingState message="Executing multi-stage MongoDB aggregation pipelines..." />;
  }

  const metrics = data?.metrics;
  const repeat = data?.repeat_customers;

  return (
    <div className="space-y-6">
      {/* Top Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 bg-white p-5 rounded-2xl border border-slate-200/80 shadow-subtle">
        <div>
          <h2 className="text-xl font-bold text-slate-900 tracking-tight">Analytics &amp; Aggregation Reports</h2>
          <p className="text-xs text-slate-500 mt-0.5">
            Aggregated entirely with MongoDB pipelines ($group, $unwind, $lookup, $project, $facet).
          </p>
        </div>

        {/* CSV Export Buttons */}
        <div className="flex flex-wrap items-center gap-2">
          <button
            onClick={() => handleExportCSV('category')}
            disabled={exporting}
            className="flex items-center gap-1.5 px-3 py-1.5 bg-slate-100 hover:bg-slate-200 text-slate-700 rounded-xl text-xs font-semibold transition"
          >
            <FileSpreadsheet className="w-3.5 h-3.5 text-emerald-600" />
            <span>Export Category CSV</span>
          </button>
          <button
            onClick={() => handleExportCSV('monthly')}
            disabled={exporting}
            className="flex items-center gap-1.5 px-3 py-1.5 bg-slate-100 hover:bg-slate-200 text-slate-700 rounded-xl text-xs font-semibold transition"
          >
            <FileSpreadsheet className="w-3.5 h-3.5 text-blue-600" />
            <span>Export Monthly CSV</span>
          </button>
          <button
            onClick={() => handleExportCSV('top_products')}
            disabled={exporting}
            className="flex items-center gap-1.5 px-3 py-1.5 bg-brand-600 hover:bg-brand-700 text-white rounded-xl text-xs font-semibold shadow-sm transition"
          >
            <Download className="w-3.5 h-3.5" />
            <span>Export Top SKUs CSV</span>
          </button>
        </div>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard
          title="Gross Sales"
          value={`$${(metrics?.total_revenue || 0).toLocaleString('en-US', { minimumFractionDigits: 2 })}`}
          subtitle="Non-cancelled order totals"
          icon={DollarSign}
          color="emerald"
        />
        <StatCard
          title="Average Order Value"
          value={`$${(metrics?.average_order_value || 0).toFixed(2)}`}
          subtitle="Computed via $avg"
          icon={ShoppingBag}
          color="blue"
        />
        <StatCard
          title="Repeat Customer Rate"
          value={`${repeat?.repeat_customer_rate || 0}%`}
          subtitle={`${repeat?.repeat_customers || 0} repeat buyers`}
          icon={Users}
          color="indigo"
        />
        <StatCard
          title="Orders per Customer"
          value={`${repeat?.average_orders_per_customer || 0}`}
          subtitle="Customer retention ratio"
          icon={TrendingUp}
          color="purple"
        />
      </div>

      {/* Charts Grid: Monthly Revenue & Category Sales */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Monthly Revenue Chart */}
        <div className="bg-white p-5 rounded-2xl border border-slate-200/80 shadow-subtle">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h3 className="text-base font-bold text-slate-900">Revenue Growth Trend</h3>
              <p className="text-xs text-slate-500">MongoDB Time-Series Aggregation by Month</p>
            </div>
            <span className="text-[11px] font-semibold text-emerald-700 bg-emerald-50 px-2.5 py-0.5 rounded-full border border-emerald-200">
              Live Pipeline
            </span>
          </div>

          <div className="h-64 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={data?.monthly_trends || []}>
                <defs>
                  <linearGradient id="analyticsRev" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#10B981" stopOpacity={0.3} />
                    <stop offset="95%" stopColor="#10B981" stopOpacity={0} />
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
                  formatter={(val: any) => [`$${Number(val).toLocaleString()}`, 'Monthly Gross']}
                  contentStyle={{ backgroundColor: '#0B132B', color: '#fff', borderRadius: '10px', fontSize: '12px' }}
                />
                <Area type="monotone" dataKey="revenue" stroke="#059669" strokeWidth={2.5} fillOpacity={1} fill="url(#analyticsRev)" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Category Sales Volume */}
        <div className="bg-white p-5 rounded-2xl border border-slate-200/80 shadow-subtle">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h3 className="text-base font-bold text-slate-900">Revenue by Category</h3>
              <p className="text-xs text-slate-500">$unwind on items &amp; $lookup with products</p>
            </div>
            <span className="text-[11px] font-semibold text-blue-700 bg-blue-50 px-2.5 py-0.5 rounded-full border border-blue-200">
              Unwound Array
            </span>
          </div>

          <div className="h-64 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={data?.category_sales || []}>
                <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#E2E8F0" />
                <XAxis dataKey="category" stroke="#94A3B8" fontSize={10} tickLine={false} interval={0} />
                <YAxis
                  stroke="#94A3B8"
                  fontSize={11}
                  tickLine={false}
                  axisLine={false}
                  tickFormatter={(val) => `$${val >= 1000 ? `${(val / 1000).toFixed(0)}k` : val}`}
                />
                <Tooltip
                  formatter={(val: any) => [`$${Number(val).toLocaleString()}`, 'Total Sales']}
                  contentStyle={{ backgroundColor: '#0B132B', color: '#fff', borderRadius: '10px', fontSize: '12px' }}
                />
                <Bar dataKey="total_revenue" radius={[6, 6, 0, 0]}>
                  {(data?.category_sales || []).map((_: any, idx: number) => (
                    <Cell key={idx} fill={PALETTE[idx % PALETTE.length]} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      {/* Two-Column: Order Status Distribution & Review Ratings */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Order Status Breakdown */}
        <div className="bg-white p-5 rounded-2xl border border-slate-200/80 shadow-subtle">
          <h3 className="text-base font-bold text-slate-900 mb-1">Order Status Lifecycle</h3>
          <p className="text-xs text-slate-500 mb-4">Grouping distribution across all orders</p>

          <div className="space-y-3">
            {(data?.status_distribution || []).map((st: any) => {
              let barColor = 'bg-slate-400';
              if (st.status === 'delivered') barColor = 'bg-emerald-500';
              else if (st.status === 'shipped') barColor = 'bg-blue-500';
              else if (st.status === 'confirmed') barColor = 'bg-indigo-500';
              else if (st.status === 'pending') barColor = 'bg-amber-500';
              else if (st.status === 'cancelled') barColor = 'bg-rose-500';

              return (
                <div key={st.status} className="text-xs">
                  <div className="flex items-center justify-between mb-1 font-semibold text-slate-700 capitalize">
                    <span>{st.status}</span>
                    <span>
                      {st.count} orders ({st.percentage}%)
                    </span>
                  </div>
                  <div className="w-full h-2 bg-slate-100 rounded-full overflow-hidden">
                    <div
                      className={`h-full rounded-full ${barColor}`}
                      style={{ width: `${st.percentage}%` }}
                    />
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {/* Review Ratings Distribution */}
        <div className="bg-white p-5 rounded-2xl border border-slate-200/80 shadow-subtle">
          <h3 className="text-base font-bold text-slate-900 mb-1">Customer Sentiment &amp; Ratings</h3>
          <p className="text-xs text-slate-500 mb-4">Rating distribution grouped 1 through 5 stars</p>

          <div className="space-y-3">
            {(data?.rating_distribution || []).map((r: any) => {
              const totalReviews = (data?.rating_distribution || []).reduce((acc: number, curr: any) => acc + curr.count, 0);
              const pct = totalReviews > 0 ? ((r.count / totalReviews) * 100).toFixed(1) : '0';

              return (
                <div key={r.rating} className="flex items-center gap-3 text-xs">
                  <div className="flex items-center gap-1 w-16 text-amber-500 font-bold shrink-0">
                    <span>{r.rating}</span>
                    <Star className="w-3.5 h-3.5 fill-amber-400" />
                  </div>
                  <div className="flex-1 h-2 bg-slate-100 rounded-full overflow-hidden">
                    <div
                      className="h-full bg-amber-400 rounded-full"
                      style={{ width: `${pct}%` }}
                    />
                  </div>
                  <span className="w-20 text-right text-slate-600 font-medium shrink-0">
                    {r.count} ({pct}%)
                  </span>
                </div>
              );
            })}
          </div>
        </div>
      </div>
    </div>
  );
};
