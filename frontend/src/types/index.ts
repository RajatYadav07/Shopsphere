export interface Product {
  id: string;
  _id?: string;
  name: string;
  sku: string;
  category: string;
  brand: string;
  description: string;
  price: number;
  stock_quantity: number;
  inventory_tracked?: boolean;
  tags: string[];
  rating_average: number;
  review_count: number;
  image_url?: string;
  source?: string;
  external_id?: string;
  created_at?: string;
  updated_at?: string;
}

export interface Customer {
  id: string;
  _id?: string;
  name: string;
  email?: string;
  phone?: string;
  address?: string;
  city?: string;
  state?: string;
  zip_code_prefix?: string;
  source?: string;
  external_id?: string;
  external_unique_id?: string;
  created_at?: string;
  total_spent?: number;
  total_orders?: number;
  average_order_value?: number;
}

export interface CustomerDetail extends Customer {
  order_history?: Order[];
}

export interface ShippingAddress {
  street?: string;
  city: string;
  state?: string;
  postal_code?: string;
  country: string;
}

export interface OrderItem {
  product_id: string;
  name: string;
  sku: string;
  unit_price: number;
  quantity: number;
  line_total: number;
  category?: string;
  freight_value?: number;
  seller_id?: string;
}

export type OrderStatus = 'pending' | 'confirmed' | 'shipped' | 'delivered' | 'cancelled';

export interface OrderPayment {
  sequential: number;
  type: string;
  installments: number;
  value: number;
}

export interface Order {
  id: string;
  _id?: string;
  customer_id: string;
  items: OrderItem[];
  shipping_address: ShippingAddress;
  subtotal: number;
  freight_total?: number;
  total_amount?: number;
  status: OrderStatus;
  notes?: string;
  source?: string;
  external_id?: string;
  is_historical?: boolean;
  payments?: OrderPayment[];
  created_at?: string;
  updated_at?: string;
  customer_name?: string;
  customer_email?: string;
}

export interface InventoryMovement {
  id: string;
  _id?: string;
  product_id: string;
  product_name?: string;
  sku?: string;
  change_quantity: number;
  reason: string;
  related_order_id?: string;
  created_at?: string;
}

export interface Review {
  id: string;
  _id?: string;
  product_id: string;
  customer_id: string;
  product_name?: string;
  customer_name?: string;
  rating: number;
  review_text: string;
  created_at?: string;
}

export interface DashboardMetrics {
  total_revenue: number;
  total_orders: number;
  total_customers: number;
  total_products: number;
  pending_orders: number;
  low_stock_products_count: number;
  average_order_value: number;
}

export interface MonthlyTrendPoint {
  month: string;
  revenue: number;
  orders_count: number;
}

export interface CategorySalesPoint {
  category: string;
  total_revenue: number;
  units_sold: number;
  order_count: number;
}

export interface TopProduct {
  product_id: string;
  name: string;
  sku: string;
  category: string;
  units_sold: number;
  total_revenue: number;
}

export interface DashboardSummary {
  metrics: DashboardMetrics;
  monthly_trends: MonthlyTrendPoint[];
  category_sales: CategorySalesPoint[];
  top_products: TopProduct[];
  recent_orders: Order[];
  low_stock_alerts: Product[];
}

export interface PaginatedResult<T> {
  items: T[];
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
  has_next: boolean;
  has_prev: boolean;
}

export interface SystemHealth {
  connected: boolean;
  database: string;
  server_version?: string;
  topology?: string;
  transactions_supported?: boolean;
  collections?: string[];
  error?: string;
}
