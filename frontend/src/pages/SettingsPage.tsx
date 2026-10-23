import React, { useEffect, useState } from 'react';
import {
  Settings,
  Database,
  Server,
  Layers,
  CheckCircle2,
  AlertCircle,
  RefreshCw,
  Zap,
  HardDrive,
  Info,
  Check,
  X
} from 'lucide-react';
import { apiClient } from '../api/client';
import { LoadingState } from '../components/EmptyState';

export const SettingsPage: React.FC = () => {
  const [stats, setStats] = useState<any>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [reindexing, setReindexing] = useState<boolean>(false);
  const [reindexSuccess, setReindexSuccess] = useState<string | null>(null);

  const fetchStats = async () => {
    try {
      setLoading(true);
      const res = await apiClient.get('/settings/stats');
      setStats(res.data?.data || null);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchStats();
  }, []);

  const handleRecreateIndexes = async () => {
    try {
      setReindexing(true);
      setReindexSuccess(null);
      await apiClient.post('/settings/recreate-indexes');
      setReindexSuccess('All unique and compound indexes verified and synchronized in MongoDB.');
      fetchStats();
      setTimeout(() => setReindexSuccess(null), 5000);
    } catch (err: any) {
      alert(`Error recreating indexes: ${err.message}`);
    } finally {
      setReindexing(false);
    }
  };

  if (loading && !stats) {
    return <LoadingState message="Querying MongoDB server parameters and collection metadata..." />;
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 bg-white p-5 rounded-2xl border border-slate-200/80 shadow-subtle">
        <div>
          <h2 className="text-xl font-bold text-slate-900 tracking-tight">Database &amp; Topology Settings</h2>
          <p className="text-xs text-slate-500 mt-0.5">
            Local MongoDB Community Server connection details, transaction capability, and storage metrics.
          </p>
        </div>

        <button
          onClick={handleRecreateIndexes}
          disabled={reindexing}
          className="flex items-center gap-1.5 px-4 py-2 bg-brand-600 hover:bg-brand-700 text-white rounded-xl text-xs font-semibold shadow-sm transition"
        >
          <Zap className={`w-4 h-4 ${reindexing ? 'animate-spin' : ''}`} />
          <span>Verify &amp; Rebuild Indexes</span>
        </button>
      </div>

      {reindexSuccess && (
        <div className="p-3 bg-emerald-50 border border-emerald-200 text-emerald-800 rounded-xl text-xs flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Check className="w-4 h-4 text-emerald-600" />
            <span className="font-medium">{reindexSuccess}</span>
          </div>
          <button onClick={() => setReindexSuccess(null)}>
            <X className="w-4 h-4 text-emerald-600" />
          </button>
        </div>
      )}

      {/* Grid: MongoDB Info Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-white p-5 rounded-2xl border border-slate-200/80 shadow-subtle flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between mb-2">
              <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Database Name</span>
              <Database className="w-4 h-4 text-brand-600" />
            </div>
            <h3 className="text-2xl font-bold font-mono text-slate-900">{stats?.database_name || 'shopsphere'}</h3>
            <p className="text-xs text-slate-500 mt-1">Local Windows Community Edition</p>
          </div>
          <div className="mt-4 pt-3 border-t border-slate-100 flex items-center gap-2 text-xs text-emerald-600 font-semibold">
            <CheckCircle2 className="w-4 h-4" />
            <span>Connection Active (127.0.0.1:27017)</span>
          </div>
        </div>

        <div className="bg-white p-5 rounded-2xl border border-slate-200/80 shadow-subtle flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between mb-2">
              <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Engine Version</span>
              <Server className="w-4 h-4 text-indigo-600" />
            </div>
            <h3 className="text-2xl font-bold font-mono text-slate-900">
              MongoDB {stats?.server_version || '8.0.x'}
            </h3>
            <p className="text-xs text-slate-500 mt-1">Topology: {stats?.topology || 'Single'}</p>
          </div>
          <div className="mt-4 pt-3 border-t border-slate-100 flex items-center gap-2 text-xs text-slate-600">
            <Info className="w-4 h-4 text-slate-400" />
            <span>64-bit Architecture on Windows</span>
          </div>
        </div>

        <div className="bg-white p-5 rounded-2xl border border-slate-200/80 shadow-subtle flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between mb-2">
              <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Multi-Doc Transactions</span>
              <HardDrive className="w-4 h-4 text-purple-600" />
            </div>
            <h3 className="text-lg font-bold text-slate-900">
              {stats?.transactions_supported ? 'ReplicaSet Enabled' : 'Safe Standalone Fallback'}
            </h3>
            <p className="text-xs text-slate-500 mt-1">
              {stats?.transactions_supported
                ? 'ACID multi-document sessions active'
                : 'Atomic two-phase commit fallback with compensation'}
            </p>
          </div>
          <div className="mt-4 pt-3 border-t border-slate-100 text-[11px] text-slate-500">
            Standard Community setup handles concurrency safely
          </div>
        </div>
      </div>

      {/* Collection Document Counts */}
      <div className="bg-white p-5 rounded-2xl border border-slate-200/80 shadow-subtle">
        <h3 className="text-base font-bold text-slate-900 mb-1">Collection Inventory &amp; Document Volume</h3>
        <p className="text-xs text-slate-500 mb-4">Real document counts retrieved from MongoDB metadata</p>

        <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3">
          {stats?.collection_document_counts &&
            Object.entries(stats.collection_document_counts).map(([col, count]: [string, any]) => (
              <div key={col} className="p-3.5 bg-slate-50 rounded-xl border border-slate-200 text-xs">
                <p className="font-mono text-[11px] text-slate-500 font-semibold truncate">{col}</p>
                <p className="text-xl font-bold text-slate-900 mt-1">{count}</p>
                <p className="text-[10px] text-slate-400 mt-0.5">documents</p>
              </div>
            ))}
        </div>
      </div>

      {/* College Viva Architecture Notes */}
      <div className="p-5 bg-gradient-to-r from-slate-900 to-navy-900 text-white rounded-2xl shadow-subtle space-y-3">
        <h3 className="text-base font-bold text-brand-300">Technical Viva Reference Note</h3>
        <p className="text-xs text-slate-300 leading-relaxed">
          In MongoDB, multi-document ACID transactions require either a Replica Set or a Sharded Cluster. Single-node standalone instances (the default for local Windows Community Server) support single-document atomicity. ShopSphere automatically inspects the cluster topology at startup: if a Replica Set is detected, it runs native multi-document ACID transactions; if running standalone, it executes an atomic two-phase reservation with automated rollback compensation on order cancellation.
        </p>
      </div>
    </div>
  );
};
