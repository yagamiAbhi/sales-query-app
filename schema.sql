-- Schema for Sales Data Database
-- Custom dataset for retail sales analysis

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "vector";
CREATE EXTENSION IF NOT EXISTS "alloydb_ai_nl";

-- Products table
CREATE TABLE IF NOT EXISTS products (
    product_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name TEXT NOT NULL,
    category TEXT NOT NULL,
    price NUMERIC(10,2) NOT NULL
);

-- Customers table
CREATE TABLE IF NOT EXISTS customers (
    customer_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL
);

-- Sales table
CREATE TABLE IF NOT EXISTS sales (
    sale_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    product_id UUID REFERENCES products(product_id),
    customer_id UUID REFERENCES customers(customer_id),
    quantity INTEGER NOT NULL,
    sale_date DATE NOT NULL,
    total_amount NUMERIC(10,2) NOT NULL
);

-- Insert sample data
INSERT INTO products (name, category, price) VALUES
('Laptop', 'Electronics', 999.99),
('Mouse', 'Electronics', 29.99),
('Book', 'Education', 19.99),
('Chair', 'Furniture', 149.99),
('Phone', 'Electronics', 699.99);

INSERT INTO customers (name, email) VALUES
('John Doe', 'john@example.com'),
('Jane Smith', 'jane@example.com'),
('Bob Johnson', 'bob@example.com');

INSERT INTO sales (product_id, customer_id, quantity, sale_date, total_amount) VALUES
((SELECT product_id FROM products WHERE name='Laptop'), (SELECT customer_id FROM customers WHERE name='John Doe'), 1, '2024-01-15', 999.99),
((SELECT product_id FROM products WHERE name='Mouse'), (SELECT customer_id FROM customers WHERE name='Jane Smith'), 2, '2024-01-16', 59.98),
((SELECT product_id FROM products WHERE name='Book'), (SELECT customer_id FROM customers WHERE name='Bob Johnson'), 3, '2024-01-17', 59.97);