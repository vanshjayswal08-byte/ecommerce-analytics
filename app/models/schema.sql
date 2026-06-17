-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 1. Customers Table
CREATE TABLE IF NOT EXISTS customers (
    id UUID PRIMARY KEY,
    name VARCHAR(255),
    email VARCHAR(255) UNIQUE,
    joined_at TIMESTAMP
);

-- 2. Orders Table
CREATE TABLE IF NOT EXISTS orders (
    id UUID PRIMARY KEY,
    customer_id UUID REFERENCES customers (id),
    amount DECIMAL(10, 2),
    created_at TIMESTAMP
);

-- 3. Refunds Table
CREATE TABLE IF NOT EXISTS refunds (
    id UUID PRIMARY KEY,
    order_id UUID REFERENCES orders(id),
    amount DECIMAL(10, 2),
    reason VARCHAR(255),
    processed_at TIMESTAMP
);

-- 4. Performance Indexes
CREATE INDEX IF NOT EXISTS idx_orders_customer_id ON orders (customer_id);
CREATE INDEX IF NOT EXISTS idx_orders_created_at ON orders (created_at);
CREATE INDEX IF NOT EXISTS idx_refunds_order_id ON refunds (order_id);

-- 5. Materialized View for Pre-aggregation
CREATE MATERIALIZED VIEW IF NOT EXISTS mv_customer_spend AS
SELECT 
    c.id AS customer_id,
    c.name,
    c.email,
    COALESCE(SUM(o.amount), 0) - COALESCE(SUM(r.amount), 0) AS net_spend
FROM customers c
LEFT JOIN orders o ON c.id = o.customer_id
LEFT JOIN refunds r ON o.id = r.order_id
GROUP BY c.id, c.name, c.email;

CREATE UNIQUE INDEX IF NOT EXISTS idx_mv_customer_spend_id ON mv_customer_spend(customer_id);