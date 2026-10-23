import React, { useEffect, useState } from 'react';
import {
  Menu,
  Search,
  Database,
  Store,
  ExternalLink,
  CheckCircle2,
  AlertCircle,
  Bell,
  Sparkles,
  Layers
} from 'lucide-react';
import { apiClient } from '../api/client';
import { SystemHealth } from '../types';

interface NavbarProps {
  currentTab: string;
  onOpenSidebar: () => void;
  isStorefront: boolean;
  setIsStorefront: (val: boolean) => void;
  onSelectTab: (tab: string) => void;
  searchQuery: string;
  setSearchQuery: (q: string) => void;
}

export const Navbar: React.FC<NavbarProps> = ({
  currentTab,
  onOpenSidebar,
  isStorefront,
  setIsStorefront,
  onSelectTab,
  searchQuery,
  setSearchQuery,
}) => {
  const [health, setHealth] = useState<SystemHealth | null>(null);

  useEffect(() => {
    const fetchHealth = async () => {
      try {
        const res = await apiClient.get('/settings/health');
        if (res.data?.data) {
          setHealth(res.data.data);
        }
      } catch (e) {
        setHealth({ connected: false, database: 'shopsphere', error: 'Unreachable' });
      }
    };
    fetchHealth();
    const interval = setInterval(fetchHealth, 15000);
    return () => clearInterval(interval);
  }, []);

  const tabTitles: Record<string, string> = {
    dashboard: 'Executive Dashboard',
    products: 'Product Catalogue Management',
    customers: 'Customer Accounts & Analytics',
    orders: 'Order Processing & Fulfillment',
    reviews: 'Customer Reviews & Ratings',
    inventory: 'Inventory & Movement Audits',
    analytics: 'Analytics & Aggregation Reports',
    concepts: 'MongoDB Concepts & Viva Lab',
    settings: 'Database & System Settings',
  };

  return (
    <header className="sticky top-0 z-30 h-16 bg-white/90 backdrop-blur-md border-b border-slate-200/80 px-4 sm:px-6 flex items-center justify-between">
      {/* Left section: Hamburger & Title */}
      <div className="flex items-center gap-3">
        <button
          onClick={onOpenSidebar}
          className="p-2 -ml-2 rounded-xl text-slate-600 hover:bg-slate-100 lg:hidden"
        >
          <Menu className="w-5 h-5" />
        </button>

        <div>
          <h1 className="text-base sm:text-lg font-bold text-slate-900 tracking-tight flex items-center gap-2">
            {isStorefront ? 'Customer Storefront' : tabTitles[currentTab] || 'Dashboard'}
            {currentTab === 'concepts' && !isStorefront && (
              <span className="hidden sm:inline-flex items-center gap-1 text-[11px] font-semibold bg-brand-50 text-brand-700 px-2.5 py-0.5 rounded-full border border-brand-200">
                <Sparkles className="w-3 h-3 text-brand-600" />
                Viva Ready
              </span>
            )}
          </h1>
        </div>
      </div>

      {/* Center Search Input */}
      {!isStorefront && (
        <div className="hidden md:flex items-center flex-1 max-w-md mx-6">
          <div className="relative w-full">
            <Search className="absolute left-3.5 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
            <input
              type="text"
              placeholder="Search products, orders, customers..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full pl-9 pr-4 py-1.5 text-xs bg-slate-100/80 hover:bg-slate-100 focus:bg-white border border-transparent focus:border-brand-500 rounded-xl outline-none transition-all placeholder:text-slate-400 text-slate-800"
            />
          </div>
        </div>
      )}

      {/* Right Controls */}
      <div className="flex items-center gap-2 sm:gap-3">
        {/* MongoDB Health Indicator */}
        <button
          onClick={() => onSelectTab('settings')}
          className={`flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-medium border transition-colors ${
            health?.connected
              ? 'bg-emerald-50 text-emerald-700 border-emerald-200 hover:bg-emerald-100/60'
              : 'bg-rose-50 text-rose-700 border-rose-200 hover:bg-rose-100/60'
          }`}
          title="Click to view Database Settings & Topology"
        >
          {health?.connected ? (
            <>
              <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" />
              <span className="hidden sm:inline">MongoDB 8.0</span>
              <span className="font-semibold">Local</span>
            </>
          ) : (
            <>
              <AlertCircle className="w-3.5 h-3.5 text-rose-600" />
              <span>DB Offline</span>
            </>
          )}
        </button>

        {/* Storefront / Admin Toggle */}
        <button
          onClick={() => setIsStorefront(!isStorefront)}
          className={`hidden sm:inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl text-xs font-semibold transition-all ${
            isStorefront
              ? 'bg-slate-900 text-white hover:bg-slate-800'
              : 'bg-brand-50 text-brand-700 border border-brand-200 hover:bg-brand-100'
          }`}
        >
          {isStorefront ? (
            <>
              <Layers className="w-3.5 h-3.5" />
              <span>Admin Console</span>
            </>
          ) : (
            <>
              <Store className="w-3.5 h-3.5 text-brand-600" />
              <span>Live Storefront</span>
            </>
          )}
        </button>

        {/* User Pill */}
        <div className="flex items-center gap-2 pl-2 border-l border-slate-200">
          <div className="w-8 h-8 rounded-full bg-gradient-to-tr from-indigo-600 to-brand-500 text-white flex items-center justify-center font-bold text-xs shadow-sm">
            DS
          </div>
          <div className="hidden lg:block text-left">
            <p className="text-xs font-bold text-slate-800 leading-tight">Data Science</p>
            <p className="text-[10px] text-slate-500 leading-tight">Viva Demo Admin</p>
          </div>
        </div>
      </div>
    </header>
  );
};
