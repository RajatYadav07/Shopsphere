import React, { useEffect, useState } from 'react';
import {
  Users,
  Search,
  Plus,
  Mail,
  Phone,
  MapPin,
  Calendar,
  ShoppingBag,
  DollarSign,
  ChevronLeft,
  ChevronRight,
  Eye,
  Trash2,
  Edit2,
  Check,
  X
} from 'lucide-react';
import { apiClient } from '../api/client';
import { Customer, CustomerDetail, PaginatedResult } from '../types';
import { Modal } from '../components/Modal';
import { StatusBadge } from '../components/StatusBadge';
import { EmptyState, LoadingState } from '../components/EmptyState';

export const CustomersPage: React.FC = () => {
  const [customers, setCustomers] = useState<Customer[]>([]);
  const [total, setTotal] = useState<number>(0);
  const [page, setPage] = useState<number>(1);
  const [pageSize] = useState<number>(15);
  const [totalPages, setTotalPages] = useState<number>(1);
  const [loading, setLoading] = useState<boolean>(true);
  const [search, setSearch] = useState<string>('');

  // Modals
  const [selectedCustomer, setSelectedCustomer] = useState<CustomerDetail | null>(null);
  const [detailLoading, setDetailLoading] = useState<boolean>(false);
  const [isAddModalOpen, setIsAddModalOpen] = useState<boolean>(false);
  const [editingCustomer, setEditingCustomer] = useState<Customer | null>(null);
  const [formError, setFormError] = useState<string | null>(null);
  const [actionSuccess, setActionSuccess] = useState<string | null>(null);

  // Form
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    phone: '',
    address: '',
    city: '',
  });

  const fetchCustomers = async () => {
    try {
      setLoading(true);
      const params: any = { page, page_size: pageSize };
      if (search.trim()) params.search = search.trim();

      const res = await apiClient.get('/customers', { params });
      const data: PaginatedResult<Customer> = res.data;
      setCustomers(data.items || []);
      setTotal(data.total || 0);
      setTotalPages(data.total_pages || 1);
    } catch (e) {
      console.error('Error fetching customers:', e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchCustomers();
  }, [page, search]);

  const viewCustomerDetail = async (id: string) => {
    try {
      setDetailLoading(true);
      const res = await apiClient.get(`/customers/${id}`);
      setSelectedCustomer(res.data?.data || null);
    } catch (err: any) {
      alert(`Error fetching customer profile: ${err.message}`);
    } finally {
      setDetailLoading(false);
    }
  };

  const handleCreateOrUpdate = async (e: React.FormEvent) => {
    e.preventDefault();
    setFormError(null);

    const payload = {
      name: formData.name.trim(),
      email: formData.email.trim().toLowerCase(),
      phone: formData.phone.trim(),
      address: formData.address.trim(),
      city: formData.city.trim(),
    };

    try {
      if (editingCustomer) {
        await apiClient.put(`/customers/${editingCustomer.id}`, payload);
        setActionSuccess(`Customer '${payload.name}' updated successfully.`);
      } else {
        await apiClient.post('/customers', payload);
        setActionSuccess(`Customer '${payload.name}' created with unique email.`);
      }
      setIsAddModalOpen(false);
      setEditingCustomer(null);
      fetchCustomers();
      setTimeout(() => setActionSuccess(null), 4000);
    } catch (err: any) {
      setFormError(err.message || 'Customer operation failed');
    }
  };

  const handleDelete = async (id: string) => {
    if (!window.confirm('Delete this customer? Note: If this customer has existing orders, MongoDB referential safeguard will reject deletion.')) {
      return;
    }
    try {
      await apiClient.delete(`/customers/${id}`);
      setActionSuccess('Customer deleted.');
      fetchCustomers();
      setTimeout(() => setActionSuccess(null), 4000);
    } catch (err: any) {
      alert(`Safeguard rejection: ${err.message}`);
    }
  };

  const openCreateModal = () => {
    setEditingCustomer(null);
    setFormData({
      name: '',
      email: '',
      phone: '+1-555-0199',
      address: '100 Silicon Way',
      city: 'San Francisco',
    });
    setFormError(null);
    setIsAddModalOpen(true);
  };

  const openEditModal = (c: Customer) => {
    setEditingCustomer(c);
    setFormData({
      name: c.name,
      email: c.email || '',
      phone: c.phone || '',
      address: c.address || '',
      city: c.city || '',
    });
    setFormError(null);
    setIsAddModalOpen(true);
  };

  return (
    <div className="space-y-6">
      {/* Action Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 bg-white p-5 rounded-2xl border border-slate-200/80 shadow-subtle">
        <div>
          <h2 className="text-xl font-bold text-slate-900 tracking-tight">Customer Accounts &amp; Lifetime Metrics</h2>
          <p className="text-xs text-slate-500 mt-0.5">
            Indexed with unique email constraint &amp; live order aggregation pipelines.
          </p>
        </div>
        <div className="flex items-center gap-3">
          <div className="relative min-w-[220px]">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
            <input
              type="text"
              placeholder="Search name, email, city..."
              value={search}
              onChange={(e) => {
                setSearch(e.target.value);
                setPage(1);
              }}
              className="w-full pl-9 pr-3 py-1.5 text-xs bg-slate-50 border border-slate-200 rounded-xl outline-none focus:border-brand-500"
            />
          </div>
          <button
            onClick={openCreateModal}
            className="flex items-center gap-1.5 px-4 py-2 bg-brand-600 hover:bg-brand-700 text-white rounded-xl text-xs font-semibold shadow-sm transition whitespace-nowrap"
          >
            <Plus className="w-4 h-4" />
            <span>Add Customer</span>
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

      {/* Customer List Table */}
      {loading ? (
        <LoadingState message="Aggregating customer metrics from MongoDB..." />
      ) : customers.length === 0 ? (
        <EmptyState
          icon={Users}
          title="No Customers Found"
          description="No customer accounts match your search. Clear the search bar or create a new customer."
          actionText="Add Customer"
          onAction={openCreateModal}
        />
      ) : (
        <div className="bg-white rounded-2xl border border-slate-200/80 shadow-subtle overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="bg-slate-50 text-slate-600 uppercase font-semibold border-b border-slate-200">
                <tr>
                  <th className="py-3 px-4">Customer</th>
                  <th className="py-3 px-4">Contact</th>
                  <th className="py-3 px-4">Location</th>
                  <th className="py-3 px-4 text-right">Lifetime Spend</th>
                  <th className="py-3 px-4 text-center">Orders</th>
                  <th className="py-3 px-4 text-right">Avg Order Value</th>
                  <th className="py-3 px-4 text-center">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {customers.map((c) => (
                  <tr key={c.id} className="hover:bg-slate-50/60 transition">
                    <td className="py-3 px-4">
                      <div className="flex items-center gap-2.5">
                        <div className="w-7 h-7 rounded-full bg-slate-200 text-slate-700 flex items-center justify-center font-bold text-xs uppercase">
                          {c.name.slice(0, 2)}
                        </div>
                        <div>
                          <div className="flex items-center gap-1.5">
                            <p className="font-bold text-slate-900">{c.name}</p>
                            {c.source === 'olist_real' && (
                              <span className="px-1.5 py-0.5 bg-blue-50 text-blue-700 text-[9px] font-semibold rounded border border-blue-200">
                                Olist
                              </span>
                            )}
                          </div>
                          <p className="text-[10px] text-slate-400 font-mono">{c.id.slice(-6)}</p>
                        </div>
                      </div>
                    </td>
                    <td className="py-3 px-4">
                      <p className="text-slate-800 font-medium">
                        {c.email || (c.source === 'olist_real' ? 'Anonymized (Olist Dataset)' : 'No email')}
                      </p>
                      <p className="text-[10px] text-slate-500">
                        {c.phone || (c.external_unique_id ? `Olist ID: ${c.external_unique_id.slice(0, 10)}...` : 'No phone')}
                      </p>
                    </td>
                    <td className="py-3 px-4 text-slate-600">
                      <div className="flex items-center gap-1">
                        <MapPin className="w-3 h-3 text-slate-400" />
                        <span>{c.city ? `${c.city}${c.state ? `, ${c.state}` : ''}` : 'Unknown'}</span>
                      </div>
                    </td>
                    <td className="py-3 px-4 text-right font-bold text-emerald-600">
                      ${(c.total_spent || 0).toLocaleString('en-US', { minimumFractionDigits: 2 })}
                    </td>
                    <td className="py-3 px-4 text-center">
                      <span className="inline-block px-2 py-0.5 rounded-full font-bold bg-slate-100 text-slate-700">
                        {c.total_orders || 0}
                      </span>
                    </td>
                    <td className="py-3 px-4 text-right font-semibold text-slate-800">
                      ${(c.average_order_value || 0).toFixed(2)}
                    </td>
                    <td className="py-3 px-4 text-center">
                      <div className="flex items-center justify-center gap-1.5">
                        <button
                          onClick={() => viewCustomerDetail(c.id)}
                          className="p-1.5 text-slate-400 hover:text-brand-600 hover:bg-slate-100 rounded-lg transition"
                          title="View Order History"
                        >
                          <Eye className="w-3.5 h-3.5" />
                        </button>
                        <button
                          onClick={() => openEditModal(c)}
                          className="p-1.5 text-slate-400 hover:text-indigo-600 hover:bg-slate-100 rounded-lg transition"
                          title="Edit Customer"
                        >
                          <Edit2 className="w-3.5 h-3.5" />
                        </button>
                        <button
                          onClick={() => handleDelete(c.id)}
                          className="p-1.5 text-slate-400 hover:text-rose-600 hover:bg-slate-100 rounded-lg transition"
                          title="Delete Customer"
                        >
                          <Trash2 className="w-3.5 h-3.5" />
                        </button>
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
          Showing {(page - 1) * pageSize + 1} to {Math.min(page * pageSize, total)} of {total} customers
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

      {/* Customer Detail & Order History Modal */}
      {selectedCustomer && (
        <Modal
          isOpen={!!selectedCustomer}
          onClose={() => setSelectedCustomer(null)}
          title={selectedCustomer.name}
          subtitle={`Customer ObjectId: ${selectedCustomer.id}`}
          maxWidth="2xl"
        >
          <div className="space-y-4 text-xs">
            {/* Quick Summary Grid */}
            <div className="grid grid-cols-3 gap-3">
              <div className="p-3 bg-slate-50 rounded-xl border border-slate-100">
                <p className="text-[11px] text-slate-500">Lifetime Spend</p>
                <p className="text-base font-bold text-emerald-600 mt-0.5">
                  ${(selectedCustomer.total_spent || 0).toFixed(2)}
                </p>
              </div>
              <div className="p-3 bg-slate-50 rounded-xl border border-slate-100">
                <p className="text-[11px] text-slate-500">Total Orders</p>
                <p className="text-base font-bold text-slate-800 mt-0.5">
                  {selectedCustomer.total_orders || 0}
                </p>
              </div>
              <div className="p-3 bg-slate-50 rounded-xl border border-slate-100">
                <p className="text-[11px] text-slate-500">Average Order Value</p>
                <p className="text-base font-bold text-brand-600 mt-0.5">
                  ${(selectedCustomer.average_order_value || 0).toFixed(2)}
                </p>
              </div>
            </div>

            {/* Profile Info */}
            <div className="p-3 bg-white rounded-xl border border-slate-200 space-y-1">
              <p className="text-slate-700">
                <strong className="text-slate-900">Email:</strong> {selectedCustomer.email}
              </p>
              <p className="text-slate-700">
                <strong className="text-slate-900">Phone:</strong> {selectedCustomer.phone || 'N/A'}
              </p>
              <p className="text-slate-700">
                <strong className="text-slate-900">Address:</strong> {selectedCustomer.address}, {selectedCustomer.city}
              </p>
            </div>

            {/* Order History */}
            <div>
              <h4 className="font-bold text-slate-900 uppercase text-[11px] tracking-wider mb-2">
                Order History (Referenced via customer_id)
              </h4>
              {!selectedCustomer.order_history || selectedCustomer.order_history.length === 0 ? (
                <p className="text-slate-500 italic p-3 bg-slate-50 rounded-xl border">No orders placed yet.</p>
              ) : (
                <div className="border border-slate-200 rounded-xl overflow-hidden">
                  <table className="w-full text-left">
                    <thead className="bg-slate-50 text-slate-600 font-semibold border-b border-slate-200">
                      <tr>
                        <th className="p-2.5">Order ID</th>
                        <th className="p-2.5">Date</th>
                        <th className="p-2.5">Items</th>
                        <th className="p-2.5">Status</th>
                        <th className="p-2.5 text-right">Total</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-slate-100">
                      {selectedCustomer.order_history.map((ord: any) => (
                        <tr key={ord.id}>
                          <td className="p-2.5 font-mono text-brand-600 font-semibold">
                            #{ord.id.slice(-6).toUpperCase()}
                          </td>
                          <td className="p-2.5 text-slate-600">
                            {new Date(ord.created_at).toLocaleDateString()}
                          </td>
                          <td className="p-2.5 text-slate-600">{ord.items.length} items</td>
                          <td className="p-2.5">
                            <StatusBadge status={ord.status} />
                          </td>
                          <td className="p-2.5 text-right font-bold text-slate-900">
                            ${ord.subtotal.toFixed(2)}
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              )}
            </div>
          </div>
        </Modal>
      )}

      {/* Add / Edit Customer Modal */}
      {isAddModalOpen && (
        <Modal
          isOpen={isAddModalOpen}
          onClose={() => setIsAddModalOpen(false)}
          title={editingCustomer ? 'Edit Customer' : 'Add New Customer'}
          subtitle="Unique index enforced on email field in customers collection"
          maxWidth="md"
        >
          <form onSubmit={handleCreateOrUpdate} className="space-y-4 text-xs">
            {formError && (
              <div className="p-3 bg-rose-50 border border-rose-200 text-rose-700 rounded-xl font-medium">
                {formError}
              </div>
            )}

            <div>
              <label className="block font-semibold text-slate-700 mb-1">Full Name *</label>
              <input
                type="text"
                required
                value={formData.name}
                onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                placeholder="e.g. John Doe"
                className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-xl outline-none focus:border-brand-500"
              />
            </div>

            <div>
              <label className="block font-semibold text-slate-700 mb-1">Email Address (Unique Index) *</label>
              <input
                type="email"
                required
                value={formData.email}
                onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                placeholder="john.doe@example.com"
                className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-xl outline-none focus:border-brand-500"
              />
            </div>

            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="block font-semibold text-slate-700 mb-1">Phone Number</label>
                <input
                  type="text"
                  value={formData.phone}
                  onChange={(e) => setFormData({ ...formData, phone: e.target.value })}
                  placeholder="+1-555-0142"
                  className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-xl outline-none focus:border-brand-500"
                />
              </div>

              <div>
                <label className="block font-semibold text-slate-700 mb-1">City</label>
                <input
                  type="text"
                  value={formData.city}
                  onChange={(e) => setFormData({ ...formData, city: e.target.value })}
                  placeholder="Austin"
                  className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-xl outline-none focus:border-brand-500"
                />
              </div>
            </div>

            <div>
              <label className="block font-semibold text-slate-700 mb-1">Street Address</label>
              <input
                type="text"
                value={formData.address}
                onChange={(e) => setFormData({ ...formData, address: e.target.value })}
                placeholder="742 Evergreen Terrace"
                className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-xl outline-none focus:border-brand-500"
              />
            </div>

            <div className="flex justify-end gap-2 pt-3 border-t border-slate-100">
              <button
                type="button"
                onClick={() => setIsAddModalOpen(false)}
                className="px-4 py-2 bg-slate-100 hover:bg-slate-200 text-slate-700 rounded-xl font-semibold"
              >
                Cancel
              </button>
              <button
                type="submit"
                className="px-5 py-2 bg-brand-600 hover:bg-brand-700 text-white rounded-xl font-semibold shadow-sm"
              >
                {editingCustomer ? 'Update Customer' : 'Save Customer to MongoDB'}
              </button>
            </div>
          </form>
        </Modal>
      )}
    </div>
  );
};
