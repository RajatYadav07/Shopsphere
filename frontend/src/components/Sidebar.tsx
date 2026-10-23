import React from 'react';
import {
  LayoutDashboard,
  Package,
  Users,
  ShoppingBag,
  Star,
  Layers,
  BarChart3,
  Cpu,
  Settings,
  Store,
  Database,
  X,
  Sparkles
} from 'lucide-react';

interface SidebarProps {
  currentTab: string;
  setCurrentTab: (tab: string) => void;
  isOpen: boolean;
  setIsOpen: (open: boolean) => void;
  isStorefront: boolean;
  setIsStorefront: (sf: boolean) => void;
}

export const Sidebar: React.FC<SidebarProps> = ({
  currentTab,
  setCurrentTab,
  isOpen,
  setIsOpen,
  isStorefront,
  setIsStorefront,
}) => {
  const navItems = [
    { id: 'dashboard', label: 'Dashboard', icon: LayoutDashboard },
    { id: 'products', label: 'Products', icon: Package },
    { id: 'customers', label: 'Customers', icon: Users },
    { id: 'orders', label: 'Orders', icon: ShoppingBag },
    { id: 'reviews', label: 'Reviews', icon: Star },
    { id: 'inventory', label: 'Inventory', icon: Layers },
    { id: 'analytics', label: 'Analytics & Reports', icon: BarChart3 },
    {
      id: 'concepts',
      label: 'MongoDB Concepts Lab',
      icon: Cpu,
      badge: 'Core Lab',
      highlight: true
    },
    { id: 'settings', label: 'Settings', icon: Settings },
  ];

  return (
    <>
      {/* Mobile backdrop */}
      {isOpen && (
        <div
          className="fixed inset-0 bg-slate-900/60 z-40 lg:hidden backdrop-blur-xs"
          onClick={() => setIsOpen(false)}
        />
      )}

      {/* Persistent Left Sidebar */}
      <aside
        className={`fixed top-0 bottom-0 left-0 z-40 w-64 bg-navy-900 text-slate-300 flex flex-col transition-transform duration-300 ease-in-out border-r border-slate-800 ${
          isOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'
        }`}
      >
        {/* Brand Header */}
        <div className="h-16 flex items-center justify-between px-6 border-b border-slate-800/80 bg-navy-950/40">
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 rounded-xl bg-gradient-to-tr from-brand-600 to-indigo-500 flex items-center justify-center text-white shadow-md shadow-brand-500/20">
              <Database className="w-5 h-5" />
            </div>
            <div>
              <div className="flex items-center gap-1.5">
                <span className="font-bold text-lg text-white tracking-tight">ShopSphere</span>
                <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse" />
              </div>
              <p className="text-[10px] uppercase font-semibold tracking-wider text-brand-400">
                MongoDB Enterprise
              </p>
            </div>
          </div>
          <button
            onClick={() => setIsOpen(false)}
            className="p-1 text-slate-400 hover:text-white lg:hidden"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Navigation List */}
        <div className="flex-1 overflow-y-auto px-3 py-4 space-y-1">
          <div className="px-3 pb-2 text-[10px] font-bold uppercase tracking-wider text-slate-500">
            Platform Modules
          </div>

          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = !isStorefront && currentTab === item.id;

            return (
              <button
                key={item.id}
                onClick={() => {
                  setIsStorefront(false);
                  setCurrentTab(item.id);
                  setIsOpen(false);
                }}
                className={`w-full flex items-center justify-between px-3.5 py-2.5 rounded-xl text-sm font-medium transition-all group ${
                  isActive
                    ? 'bg-brand-600 text-white shadow-sm shadow-brand-600/30'
                    : item.highlight
                    ? 'text-brand-300 hover:bg-slate-800/80 hover:text-white border border-brand-500/30 bg-brand-500/10'
                    : 'text-slate-300 hover:bg-slate-800/60 hover:text-white'
                }`}
              >
                <div className="flex items-center gap-3">
                  <Icon
                    className={`w-4 h-4 transition-transform group-hover:scale-110 ${
                      isActive ? 'text-white' : item.highlight ? 'text-brand-400' : 'text-slate-400'
                    }`}
                  />
                  <span>{item.label}</span>
                </div>
                {item.badge && (
                  <span
                    className={`text-[10px] font-bold px-2 py-0.5 rounded-full tracking-wide ${
                      isActive
                        ? 'bg-white/20 text-white'
                        : 'bg-brand-500/20 text-brand-300 border border-brand-400/30'
                    }`}
                  >
                    {item.badge}
                  </span>
                )}
              </button>
            );
          })}
        </div>

        {/* Storefront Switcher Footer */}
        <div className="p-4 border-t border-slate-800/80 bg-navy-950/60">
          <button
            onClick={() => {
              setIsStorefront(!isStorefront);
              setIsOpen(false);
            }}
            className={`w-full flex items-center justify-center gap-2.5 px-4 py-2.5 rounded-xl text-xs font-semibold transition-all shadow-sm ${
              isStorefront
                ? 'bg-emerald-600 hover:bg-emerald-700 text-white'
                : 'bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700'
            }`}
          >
            {isStorefront ? (
              <>
                <LayoutDashboard className="w-4 h-4" />
                <span>Return to Admin Console</span>
              </>
            ) : (
              <>
                <Store className="w-4 h-4 text-emerald-400" />
                <span>Open Customer Storefront</span>
              </>
            )}
          </button>

          <div className="mt-3 flex items-center justify-between text-[11px] text-slate-500 px-1">
            <span>MongoDB Atlas</span>
            <span className="flex items-center gap-1 text-emerald-400">
              <span className="w-1.5 h-1.5 rounded-full bg-emerald-400" />
              Connected
            </span>
          </div>
        </div>
      </aside>
    </>
  );
};
