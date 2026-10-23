import React, { useState } from 'react';
import { Sidebar } from './components/Sidebar';
import { Navbar } from './components/Navbar';
import { DashboardPage } from './pages/DashboardPage';
import { ProductsPage } from './pages/ProductsPage';
import { CustomersPage } from './pages/CustomersPage';
import { OrdersPage } from './pages/OrdersPage';
import { InventoryPage } from './pages/InventoryPage';
import { ReviewsPage } from './pages/ReviewsPage';
import { AnalyticsPage } from './pages/AnalyticsPage';
import { ConceptsLabPage } from './pages/ConceptsLabPage';
import { SettingsPage } from './pages/SettingsPage';
import { StorefrontPage } from './pages/StorefrontPage';

export function App() {
  const getInitialTab = () => {
    const hash = window.location.hash.replace('#', '').trim();
    if (['dashboard', 'products', 'customers', 'orders', 'inventory', 'reviews', 'analytics', 'concepts', 'settings'].includes(hash)) {
      return hash;
    }
    return 'dashboard';
  };

  const [currentTab, setCurrentTabState] = useState<string>(getInitialTab);
  const [isSidebarOpen, setIsSidebarOpen] = useState<boolean>(false);
  const [isStorefront, setIsStorefront] = useState<boolean>(() => window.location.hash === '#storefront');
  const [searchQuery, setSearchQuery] = useState<string>('');

  const setCurrentTab = (tab: string) => {
    window.location.hash = tab;
    setCurrentTabState(tab);
  };

  React.useEffect(() => {
    const onHashChange = () => {
      const hash = window.location.hash.replace('#', '').trim();
      if (hash === 'storefront') {
        setIsStorefront(true);
      } else if (['dashboard', 'products', 'customers', 'orders', 'inventory', 'reviews', 'analytics', 'concepts', 'settings'].includes(hash)) {
        setIsStorefront(false);
        setCurrentTabState(hash);
      }
    };
    window.addEventListener('hashchange', onHashChange);
    return () => window.removeEventListener('hashchange', onHashChange);
  }, []);

  const renderCurrentModule = () => {
    if (isStorefront) {
      return <StorefrontPage />;
    }

    switch (currentTab) {
      case 'dashboard':
        return <DashboardPage onNavigate={setCurrentTab} />;
      case 'products':
        return <ProductsPage />;
      case 'customers':
        return <CustomersPage />;
      case 'orders':
        return <OrdersPage />;
      case 'inventory':
        return <InventoryPage />;
      case 'reviews':
        return <ReviewsPage />;
      case 'analytics':
        return <AnalyticsPage />;
      case 'concepts':
        return <ConceptsLabPage />;
      case 'settings':
        return <SettingsPage />;
      default:
        return <DashboardPage onNavigate={setCurrentTab} />;
    }
  };

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900 flex">
      {/* Persistent Left Sidebar */}
      <Sidebar
        currentTab={currentTab}
        setCurrentTab={setCurrentTab}
        isOpen={isSidebarOpen}
        setIsOpen={setIsSidebarOpen}
        isStorefront={isStorefront}
        setIsStorefront={setIsStorefront}
      />

      {/* Main App Content Area */}
      <div className="flex-1 flex flex-col min-w-0 lg:pl-64">
        {/* Sticky Top Navbar */}
        <Navbar
          currentTab={currentTab}
          onOpenSidebar={() => setIsSidebarOpen(true)}
          isStorefront={isStorefront}
          setIsStorefront={setIsStorefront}
          onSelectTab={setCurrentTab}
          searchQuery={searchQuery}
          setSearchQuery={setSearchQuery}
        />

        {/* Dynamic Page View Body */}
        <main className="flex-1 p-4 sm:p-6 lg:p-8 max-w-7xl w-full mx-auto">
          {renderCurrentModule()}
        </main>
      </div>
    </div>
  );
}

export default App;
