import React, { useEffect, useState } from 'react';
import {
  Star,
  Plus,
  Trash2,
  Edit2,
  Search,
  ChevronLeft,
  ChevronRight,
  Check,
  X,
  MessageSquare,
  ThumbsUp
} from 'lucide-react';
import { apiClient } from '../api/client';
import { Customer, PaginatedResult, Product, Review } from '../types';
import { Modal } from '../components/Modal';
import { LoadingState } from '../components/EmptyState';

export const ReviewsPage: React.FC = () => {
  const [reviews, setReviews] = useState<Review[]>([]);
  const [total, setTotal] = useState<number>(0);
  const [page, setPage] = useState<number>(1);
  const [pageSize] = useState<number>(12);
  const [totalPages, setTotalPages] = useState<number>(1);
  const [loading, setLoading] = useState<boolean>(true);
  const [ratingFilter, setRatingFilter] = useState<string>('');

  // Modals & Forms
  const [isAddModalOpen, setIsAddModalOpen] = useState<boolean>(false);
  const [availableProducts, setAvailableProducts] = useState<Product[]>([]);
  const [availableCustomers, setAvailableCustomers] = useState<Customer[]>([]);
  const [newReviewProductId, setNewReviewProductId] = useState<string>('');
  const [newReviewCustomerId, setNewReviewCustomerId] = useState<string>('');
  const [newReviewRating, setNewReviewRating] = useState<number>(5);
  const [newReviewText, setNewReviewText] = useState<string>('');
  const [actionSuccess, setActionSuccess] = useState<string | null>(null);

  const fetchReviews = async () => {
    try {
      setLoading(true);
      const params: any = { page, page_size: pageSize };
      if (ratingFilter) params.rating = parseInt(ratingFilter);

      const res = await apiClient.get('/reviews', { params });
      const data: PaginatedResult<Review> = res.data;
      setReviews(data.items || []);
      setTotal(data.total || 0);
      setTotalPages(data.total_pages || 1);
    } catch (e) {
      console.error('Error fetching reviews:', e);
    } finally {
      setLoading(false);
    }
  };

  const loadFormDependencies = async () => {
    try {
      const [pRes, cRes] = await Promise.all([
        apiClient.get('/products?page=1&page_size=50'),
        apiClient.get('/customers?page=1&page_size=50'),
      ]);
      const prods = pRes.data?.items || [];
      const custs = cRes.data?.items || [];
      setAvailableProducts(prods);
      setAvailableCustomers(custs);
      if (prods.length > 0) setNewReviewProductId(prods[0].id);
      if (custs.length > 0) setNewReviewCustomerId(custs[0].id);
    } catch (e) {
      console.error('Error loading review dependencies:', e);
    }
  };

  useEffect(() => {
    fetchReviews();
  }, [page, ratingFilter]);

  const handleCreateReview = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await apiClient.post('/reviews', {
        product_id: newReviewProductId,
        customer_id: newReviewCustomerId,
        rating: newReviewRating,
        review_text: newReviewText.trim(),
      });
      setIsAddModalOpen(false);
      setNewReviewText('');
      setActionSuccess('Review created! MongoDB aggregation recalculated product rating & review count.');
      fetchReviews();
      setTimeout(() => setActionSuccess(null), 5000);
    } catch (err: any) {
      alert(`Error submitting review: ${err.message}`);
    }
  };

  const handleDeleteReview = async (id: string) => {
    if (!window.confirm('Delete this review? Product rating average will be dynamically updated.')) return;
    try {
      await apiClient.delete(`/reviews/${id}`);
      setActionSuccess('Review deleted. Ratings recalculated.');
      fetchReviews();
      setTimeout(() => setActionSuccess(null), 4000);
    } catch (err: any) {
      alert(`Delete error: ${err.message}`);
    }
  };

  return (
    <div className="space-y-6">
      {/* Action Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 bg-white p-5 rounded-2xl border border-slate-200/80 shadow-subtle">
        <div>
          <h2 className="text-xl font-bold text-slate-900 tracking-tight">Customer Reviews &amp; Ratings</h2>
          <p className="text-xs text-slate-500 mt-0.5">
            Real feedback linked to products &amp; customers with automated rating aggregations.
          </p>
        </div>
        <div className="flex items-center gap-2.5">
          <select
            value={ratingFilter}
            onChange={(e) => {
              setRatingFilter(e.target.value);
              setPage(1);
            }}
            className="px-3 py-2 bg-slate-50 border border-slate-200 rounded-xl text-xs text-slate-700 font-medium outline-none focus:border-brand-500"
          >
            <option value="">All Star Ratings</option>
            <option value="5">5 Stars</option>
            <option value="4">4 Stars</option>
            <option value="3">3 Stars</option>
            <option value="2">2 Stars</option>
            <option value="1">1 Star</option>
          </select>
          <button
            onClick={() => {
              loadFormDependencies();
              setIsAddModalOpen(true);
            }}
            className="flex items-center gap-1.5 px-4 py-2 bg-brand-600 hover:bg-brand-700 text-white rounded-xl text-xs font-semibold shadow-sm transition"
          >
            <Plus className="w-4 h-4" />
            <span>Add Review</span>
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

      {/* Reviews Grid */}
      {loading ? (
        <LoadingState message="Fetching customer reviews from MongoDB..." />
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
          {reviews.map((rev) => (
            <div
              key={rev.id}
              className="bg-white rounded-2xl p-5 border border-slate-200/80 shadow-subtle flex flex-col justify-between hover:shadow-card transition"
            >
              <div>
                {/* Header: Product & Stars */}
                <div className="flex items-start justify-between gap-2 mb-2">
                  <div>
                    <h3 className="font-bold text-slate-900 text-xs line-clamp-1">{rev.product_name}</h3>
                    <p className="text-[10px] text-slate-400 font-mono">ID: {rev.product_id.slice(-6)}</p>
                  </div>
                  <div className="flex items-center text-amber-400 shrink-0">
                    {[...Array(5)].map((_, i) => (
                      <Star
                        key={i}
                        className={`w-3.5 h-3.5 ${
                          i < rev.rating ? 'fill-amber-400 text-amber-400' : 'text-slate-200'
                        }`}
                      />
                    ))}
                  </div>
                </div>

                {/* Review Text */}
                <p className="text-xs text-slate-600 italic leading-relaxed my-3 bg-slate-50/70 p-3 rounded-xl border border-slate-100">
                  "{rev.review_text}"
                </p>
              </div>

              {/* Author & Actions Footer */}
              <div className="flex items-center justify-between pt-3 border-t border-slate-100 text-[11px] text-slate-500">
                <div>
                  <p className="font-semibold text-slate-800">{rev.customer_name || 'Verified Buyer'}</p>
                  <p className="text-[10px] text-slate-400">
                    {rev.created_at ? new Date(rev.created_at).toLocaleDateString() : 'Recent'}
                  </p>
                </div>
                <button
                  onClick={() => handleDeleteReview(rev.id)}
                  className="p-1.5 text-slate-400 hover:text-rose-600 hover:bg-slate-100 rounded-lg transition"
                  title="Delete Review"
                >
                  <Trash2 className="w-3.5 h-3.5" />
                </button>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Pagination */}
      <div className="flex items-center justify-between text-xs text-slate-500 pt-2">
        <p>
          Showing {(page - 1) * pageSize + 1} to {Math.min(page * pageSize, total)} of {total} reviews
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

      {/* Add Review Modal */}
      {isAddModalOpen && (
        <Modal
          isOpen={isAddModalOpen}
          onClose={() => setIsAddModalOpen(false)}
          title="Submit Customer Review"
          subtitle="Recalculates average rating and review count on product document via MongoDB aggregation"
          maxWidth="md"
        >
          <form onSubmit={handleCreateReview} className="space-y-4 text-xs">
            <div>
              <label className="block font-semibold text-slate-700 mb-1">Target Product *</label>
              <select
                required
                value={newReviewProductId}
                onChange={(e) => setNewReviewProductId(e.target.value)}
                className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-xl outline-none focus:border-brand-500 font-medium"
              >
                {availableProducts.map((p) => (
                  <option key={p.id} value={p.id}>
                    {p.name} ({p.sku})
                  </option>
                ))}
              </select>
            </div>

            <div>
              <label className="block font-semibold text-slate-700 mb-1">Customer Author *</label>
              <select
                required
                value={newReviewCustomerId}
                onChange={(e) => setNewReviewCustomerId(e.target.value)}
                className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-xl outline-none focus:border-brand-500 font-medium"
              >
                {availableCustomers.map((c) => (
                  <option key={c.id} value={c.id}>
                    {c.name} ({c.email})
                  </option>
                ))}
              </select>
            </div>

            <div>
              <label className="block font-semibold text-slate-700 mb-1">Rating (1 to 5 Stars) *</label>
              <div className="flex items-center gap-2">
                {[1, 2, 3, 4, 5].map((star) => (
                  <button
                    key={star}
                    type="button"
                    onClick={() => setNewReviewRating(star)}
                    className="p-1 hover:scale-110 transition"
                  >
                    <Star
                      className={`w-6 h-6 ${
                        star <= newReviewRating ? 'fill-amber-400 text-amber-400' : 'text-slate-300'
                      }`}
                    />
                  </button>
                ))}
                <span className="font-bold text-slate-800 ml-2">{newReviewRating} out of 5</span>
              </div>
            </div>

            <div>
              <label className="block font-semibold text-slate-700 mb-1">Review Feedback *</label>
              <textarea
                rows={4}
                required
                value={newReviewText}
                onChange={(e) => setNewReviewText(e.target.value)}
                placeholder="Share your authentic experience with this product..."
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
                Post Review to MongoDB
              </button>
            </div>
          </form>
        </Modal>
      )}
    </div>
  );
};
