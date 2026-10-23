import React, { useEffect, useState } from 'react';
import {
  ShoppingBag,
  Search,
  Star,
  Plus,
  Minus,
  Trash2,
  CheckCircle,
  ArrowRight,
  X,
  CreditCard,
  Truck,
  Shield,
  Layers
} from 'lucide-react';
import { apiClient } from '../api/client';
import { Customer, Product } from '../types';
import { Modal } from '../components/Modal';
import { LoadingState } from '../components/EmptyState';

interface CartItem {
  product: Product;
  quantity: number;
}

export const StorefrontPage: React.FC = () => {
  const [products, setProducts] = useState<Product[]>([]);
  const [categories, setCategories] = useState<string[]>([]);
  const [selectedCategory, setSelectedCategory] = useState<string>('');
  const [search, setSearch] = useState<string>('');
  const [loading, setLoading] = useState<boolean>(true);

  // Cart State
  const [cart, setCart] = useState<CartItem[]>([]);
  const [isCartOpen, setIsCartOpen] = useState<boolean>(false);
  const [isCheckoutOpen, setIsCheckoutOpen] = useState<boolean>(false);
  const [selectedProduct, setSelectedProduct] = useState<Product | null>(null);

  // Checkout Form
  const [customers, setCustomers] = useState<Customer[]>([]);
  const [selectedCustomerId, setSelectedCustomerId] = useState<string>('');
  const [street, setStreet] = useState<string>('450 Innovation Parkway');
  const [city, setCity] = useState<string>('San Jose');
  const [zip, setZip] = useState<string>('95134');
  const [orderSuccess, setOrderSuccess] = useState<any>(null);
  const [checkoutError, setCheckoutError] = useState<string | null>(null);

  const fetchStoreData = async () => {
    try {
      setLoading(true);
      const params: any = { page: 1, page_size: 24 };
      if (selectedCategory) params.category = selectedCategory;
      if (search.trim()) params.search = search.trim();

      const [pRes, cRes, custRes] = await Promise.all([
        apiClient.get('/products', { params }),
        apiClient.get('/products/meta/categories'),
        apiClient.get('/customers?page=1&page_size=20'),
      ]);

      setProducts(pRes.data?.items || []);
      setCategories(cRes.data || []);
      const custs = custRes.data?.items || [];
      setCustomers(custs);
      if (custs.length > 0) setSelectedCustomerId(custs[0].id);
    } catch (e) {
      console.error('Error fetching storefront data:', e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchStoreData();
  }, [selectedCategory, search]);

  const addToCart = (product: Product) => {
    setCart((prev) => {
      const existing = prev.find((item) => item.product.id === product.id);
      const maxQty = product.inventory_tracked ? Math.max(product.stock_quantity, 1) : 99;
      if (existing) {
        return prev.map((item) =>
          item.product.id === product.id
            ? { ...item, quantity: Math.min(item.quantity + 1, maxQty) }
            : item
        );
      }
      return [...prev, { product, quantity: 1 }];
    });
    setIsCartOpen(true);
  };

  const updateQuantity = (productId: string, delta: number) => {
    setCart((prev) =>
      prev
        .map((item) => {
          if (item.product.id === productId) {
            const newQty = item.quantity + delta;
            const maxQty = item.product.inventory_tracked ? Math.max(item.product.stock_quantity, 1) : 99;
            return newQty > 0 ? { ...item, quantity: Math.min(newQty, maxQty) } : null;
          }
          return item;
        })
        .filter(Boolean) as CartItem[]
    );
  };

  const cartSubtotal = cart.reduce((sum, item) => sum + item.product.price * item.quantity, 0);

  const handleCheckoutSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setCheckoutError(null);

    if (cart.length === 0) {
      setCheckoutError('Your cart is empty');
      return;
    }

    const payload = {
      customer_id: selectedCustomerId,
      items: cart.map((item) => ({
        product_id: item.product.id,
        quantity: item.quantity,
      })),
      shipping_address: {
        street,
        city,
        state: 'CA',
        postal_code: zip,
        country: 'USA',
      },
    };

    try {
      const res = await apiClient.post('/orders', payload);
      setOrderSuccess(res.data?.data);
      setCart([]);
      setIsCheckoutOpen(false);
      fetchStoreData();
    } catch (err: any) {
      setCheckoutError(err.message || 'Order creation failed');
    }
  };

  return (
    <div className="space-y-6">
      {/* Storefront Hero Banner */}
      <div className="relative rounded-3xl bg-gradient-to-r from-blue-900 via-indigo-900 to-navy-900 text-white p-8 overflow-hidden shadow-card">
        <div className="relative z-10 max-w-xl">
          <span className="text-xs font-semibold px-3 py-1 rounded-full bg-blue-500/30 text-blue-200 border border-blue-400/30">
            Customer Experience Mode
          </span>
          <h2 className="text-3xl font-extrabold mt-3 tracking-tight">Shop the Latest Tech Catalogue</h2>
          <p className="text-slate-200 text-xs mt-2 leading-relaxed">
            Connected to the same local MongoDB backend as the Admin Dashboard. Every checkout automatically creates real Order and Inventory Movement records.
          </p>
        </div>

        {/* Floating Cart Trigger */}
        <div className="absolute right-8 top-8 z-10">
          <button
            onClick={() => setIsCartOpen(true)}
            className="flex items-center gap-2.5 px-4 py-2.5 bg-white text-slate-900 rounded-2xl text-xs font-bold shadow-float hover:bg-slate-50 transition"
          >
            <ShoppingBag className="w-4 h-4 text-brand-600" />
            <span>Bag ({cart.reduce((sum, i) => sum + i.quantity, 0)})</span>
            <span className="text-brand-600 font-extrabold">${cartSubtotal.toFixed(2)}</span>
          </button>
        </div>
      </div>

      {/* Filter and Search Bar */}
      <div className="bg-white p-4 rounded-2xl border border-slate-200/80 shadow-subtle flex flex-wrap items-center justify-between gap-3 text-xs">
        <div className="relative flex-1 min-w-[220px] max-w-md">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
          <input
            type="text"
            placeholder="Search headphones, monitors, keyboards..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="w-full pl-9 pr-3 py-2 bg-slate-50 border border-slate-200 rounded-xl outline-none focus:border-brand-500 text-slate-800"
          />
        </div>

        <div className="flex flex-wrap items-center gap-1.5">
          <button
            onClick={() => setSelectedCategory('')}
            className={`px-3 py-1.5 rounded-xl font-semibold transition ${
              selectedCategory === '' ? 'bg-slate-900 text-white' : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
            }`}
          >
            All Products
          </button>
          {categories.map((c) => (
            <button
              key={c}
              onClick={() => setSelectedCategory(c)}
              className={`px-3 py-1.5 rounded-xl font-semibold transition ${
                selectedCategory === c ? 'bg-slate-900 text-white' : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
              }`}
            >
              {c}
            </button>
          ))}
        </div>
      </div>

      {/* Product Cards Grid */}
      {loading ? (
        <LoadingState message="Loading available items from MongoDB catalogue..." />
      ) : products.length === 0 ? (
        <div className="p-12 text-center bg-white rounded-2xl border border-slate-200">
          <ShoppingBag className="w-10 h-10 text-slate-400 mx-auto mb-2" />
          <h3 className="text-base font-bold text-slate-800">No In-Stock Products Match Filter</h3>
          <p className="text-xs text-slate-500 mt-1">Try switching categories or clearing search.</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 xl:grid-cols-4 gap-5">
          {products.map((p) => (
            <div
              key={p.id}
              className="bg-white rounded-2xl border border-slate-200/80 shadow-subtle hover:shadow-card transition flex flex-col justify-between overflow-hidden group"
            >
              <div className="p-4">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-[10px] font-semibold text-brand-600 bg-brand-50 px-2 py-0.5 rounded">
                    {p.category}
                  </span>
                  <span className="text-[10px] font-bold text-slate-400 font-mono">{p.sku}</span>
                </div>

                <h3
                  onClick={() => setSelectedProduct(p)}
                  className="font-bold text-slate-900 text-sm line-clamp-1 group-hover:text-brand-600 cursor-pointer transition"
                >
                  {p.name}
                </h3>
                <p className="text-xs text-slate-500 mt-0.5">{p.brand}</p>

                <div className="flex items-center gap-1.5 mt-2">
                  <div className="flex items-center text-amber-400">
                    <Star className="w-3.5 h-3.5 fill-amber-400" />
                    <span className="text-xs font-bold text-slate-800 ml-1">
                      {p.rating_average ? p.rating_average.toFixed(1) : '0.0'}
                    </span>
                  </div>
                  <span className="text-[10px] text-slate-400">({p.review_count} ratings)</span>
                </div>

                <p className="text-xs text-slate-500 line-clamp-2 mt-2 leading-relaxed">
                  {p.description || 'Premium electronics accessory.'}
                </p>
              </div>

              <div className="px-4 py-3 bg-slate-50 border-t border-slate-100 flex items-center justify-between">
                <div>
                  <span className="text-base font-extrabold text-slate-900">${p.price.toFixed(2)}</span>
                  <p className="text-[10px] text-slate-400">
                    {p.inventory_tracked ? `${p.stock_quantity} left` : 'Catalog item'}
                  </p>
                </div>
                <button
                  onClick={() => addToCart(p)}
                  className="flex items-center gap-1.5 px-3.5 py-1.5 bg-brand-600 hover:bg-brand-700 text-white rounded-xl text-xs font-semibold shadow-xs transition"
                >
                  <Plus className="w-3.5 h-3.5" />
                  <span>Add to Bag</span>
                </button>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Cart Drawer Modal */}
      {isCartOpen && (
        <Modal
          isOpen={isCartOpen}
          onClose={() => setIsCartOpen(false)}
          title="Shopping Cart"
          subtitle={`${cart.reduce((sum, i) => sum + i.quantity, 0)} items ready for checkout`}
          maxWidth="md"
        >
          {cart.length === 0 ? (
            <div className="text-center py-8">
              <ShoppingBag className="w-10 h-10 text-slate-300 mx-auto mb-2" />
              <p className="text-xs text-slate-500">Your bag is currently empty.</p>
            </div>
          ) : (
            <div className="space-y-4 text-xs">
              <div className="space-y-2.5 max-h-64 overflow-y-auto pr-1">
                {cart.map((item) => (
                  <div
                    key={item.product.id}
                    className="p-3 bg-slate-50 rounded-xl border border-slate-100 flex items-center justify-between"
                  >
                    <div>
                      <h4 className="font-bold text-slate-900">{item.product.name}</h4>
                      <p className="text-[11px] text-slate-500">${item.product.price} each</p>
                    </div>
                    <div className="flex items-center gap-2">
                      <div className="flex items-center bg-white border border-slate-200 rounded-lg">
                        <button
                          onClick={() => updateQuantity(item.product.id, -1)}
                          className="p-1 text-slate-500 hover:text-slate-800"
                        >
                          <Minus className="w-3 h-3" />
                        </button>
                        <span className="px-2 font-bold text-slate-800">{item.quantity}</span>
                        <button
                          onClick={() => updateQuantity(item.product.id, 1)}
                          className="p-1 text-slate-500 hover:text-slate-800"
                        >
                          <Plus className="w-3 h-3" />
                        </button>
                      </div>
                      <span className="font-bold text-slate-900 w-14 text-right">
                        ${(item.product.price * item.quantity).toFixed(2)}
                      </span>
                    </div>
                  </div>
                ))}
              </div>

              <div className="pt-3 border-t border-slate-100 flex justify-between items-center text-sm font-bold text-slate-900">
                <span>Subtotal</span>
                <span>${cartSubtotal.toFixed(2)}</span>
              </div>

              <button
                onClick={() => {
                  setIsCartOpen(false);
                  setIsCheckoutOpen(true);
                }}
                className="w-full py-2.5 bg-brand-600 hover:bg-brand-700 text-white rounded-xl text-xs font-bold shadow-sm transition flex items-center justify-center gap-2"
              >
                <span>Proceed to Order Confirmation</span>
                <ArrowRight className="w-4 h-4" />
              </button>
            </div>
          )}
        </Modal>
      )}

      {/* Checkout Modal */}
      {isCheckoutOpen && (
        <Modal
          isOpen={isCheckoutOpen}
          onClose={() => setIsCheckoutOpen(false)}
          title="Place Order via Demo Customer"
          subtitle="Creates actual order in MongoDB & decrements inventory atomically"
          maxWidth="md"
        >
          <form onSubmit={handleCheckoutSubmit} className="space-y-4 text-xs">
            {checkoutError && (
              <div className="p-3 bg-rose-50 border border-rose-200 text-rose-700 rounded-xl font-medium">
                {checkoutError}
              </div>
            )}

            <div>
              <label className="block font-semibold text-slate-700 mb-1">Select Customer *</label>
              <select
                required
                value={selectedCustomerId}
                onChange={(e) => setSelectedCustomerId(e.target.value)}
                className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-xl outline-none focus:border-brand-500 font-medium"
              >
                {customers.map((c) => (
                  <option key={c.id} value={c.id}>
                    {c.name} {c.email ? `(${c.email})` : c.city ? `(${c.city}, ${c.state})` : '(Anonymized)'}
                  </option>
                ))}
              </select>
            </div>

            <div>
              <label className="block font-semibold text-slate-700 mb-1">Shipping Street Address *</label>
              <input
                type="text"
                required
                value={street}
                onChange={(e) => setStreet(e.target.value)}
                className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-xl outline-none focus:border-brand-500"
              />
            </div>

            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="block font-semibold text-slate-700 mb-1">City *</label>
                <input
                  type="text"
                  required
                  value={city}
                  onChange={(e) => setCity(e.target.value)}
                  className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-xl outline-none focus:border-brand-500"
                />
              </div>
              <div>
                <label className="block font-semibold text-slate-700 mb-1">Zip Code *</label>
                <input
                  type="text"
                  required
                  value={zip}
                  onChange={(e) => setZip(e.target.value)}
                  className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-xl outline-none focus:border-brand-500"
                />
              </div>
            </div>

            <div className="p-3 bg-slate-50 rounded-xl border flex items-center justify-between text-xs">
              <span className="font-semibold text-slate-700">Total Order Amount:</span>
              <span className="text-base font-extrabold text-slate-900">${cartSubtotal.toFixed(2)}</span>
            </div>

            <div className="flex justify-end gap-2 pt-2 border-t border-slate-100">
              <button
                type="button"
                onClick={() => setIsCheckoutOpen(false)}
                className="px-4 py-2 bg-slate-100 hover:bg-slate-200 text-slate-700 rounded-xl font-semibold"
              >
                Cancel
              </button>
              <button
                type="submit"
                className="px-5 py-2 bg-brand-600 hover:bg-brand-700 text-white rounded-xl font-bold shadow-sm"
              >
                Confirm &amp; Place Order
              </button>
            </div>
          </form>
        </Modal>
      )}

      {/* Success Order Confirmation Modal */}
      {orderSuccess && (
        <Modal
          isOpen={!!orderSuccess}
          onClose={() => setOrderSuccess(null)}
          title="Order Created in MongoDB!"
          subtitle={`Document ObjectId: ${orderSuccess.id}`}
          maxWidth="md"
        >
          <div className="text-center space-y-3 py-2 text-xs">
            <div className="w-12 h-12 rounded-full bg-emerald-100 text-emerald-600 flex items-center justify-center mx-auto">
              <CheckCircle className="w-6 h-6" />
            </div>
            <h4 className="text-base font-bold text-slate-900">
              Order #{orderSuccess.id.slice(-6).toUpperCase()} Confirmed
            </h4>
            <p className="text-slate-600 leading-relaxed">
              Total <strong>${orderSuccess.subtotal.toFixed(2)}</strong> was committed to the database. Inventory levels decremented atomically with snapshots stored in embedded format.
            </p>
            <button
              onClick={() => setOrderSuccess(null)}
              className="mt-4 px-5 py-2 bg-slate-900 text-white rounded-xl font-semibold hover:bg-slate-800 transition"
            >
              Continue Shopping
            </button>
          </div>
        </Modal>
      )}
    </div>
  );
};
