# Sales Data Query Project

This project demonstrates an AI-enabled database feature using AlloyDB for PostgreSQL. It allows users to query a custom sales dataset using natural language and receive meaningful results.

## Use Case
Querying sales data for a retail company to analyze products, customers, and transactions.

## Features
- Natural language to SQL conversion using AlloyDB AI
- Custom dataset with products, customers, and sales tables
- REST API for querying

## Setup
1. Set up AlloyDB instance with AI enabled
2. Set DATABASE_URL environment variable
3. Run schema.sql to create tables and insert sample data
4. Run the Flask app

## API Usage
POST /api/query
Body: {"nl_query": "What are the top selling products?"}

Returns generated SQL and query results.