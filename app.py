# Sales Data Query App
# AI-enabled database feature using AlloyDB for PostgreSQL
# Allows natural language queries on sales data

import os
import json
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Configuration
DATABASE_URL = os.getenv("DATABASE_URL")

engine = None
try:
    if not DATABASE_URL:
        raise ValueError("DATABASE_URL is not set")
    engine = create_engine(DATABASE_URL, pool_pre_ping=True)
except Exception as e:
    print(f"Database connection error: {e}")

@app.route('/')
def home():
    return "Sales Data Query App - Use /api/query with POST and 'nl_query' parameter"

@app.route('/api/query', methods=['POST'])
def query_sales():
    if engine is None:
        return jsonify({"error": "Database not connected"}), 500

    data = request.json
    nl_query = data.get('nl_query')
    if not nl_query:
        return jsonify({"error": "No natural language query provided"}), 400

    try:
        with engine.connect() as conn:
            # Generate SQL from natural language using AlloyDB AI
            prompt = f"""
Generate a PostgreSQL SQL query for the following natural language query: "{nl_query}".
The database has the following tables:
- products: product_id (uuid), name (text), category (text), price (numeric)
- customers: customer_id (uuid), name (text), email (text)
- sales: sale_id (uuid), product_id (uuid), customer_id (uuid), quantity (integer), sale_date (date), total_amount (numeric)

Return only the SQL query, no explanations or markdown.
"""
            gen_query = text("SELECT ai.generate_text(:prompt, model_id => 'gemini-3-flash-preview') as generated_sql")
            result = conn.execute(gen_query, {"prompt": prompt})
            generated_sql = result.fetchone()[0].strip()

            # Remove any markdown if present
            if generated_sql.startswith('```sql'):
                generated_sql = generated_sql[6:]
            if generated_sql.endswith('```'):
                generated_sql = generated_sql[:-3]
            generated_sql = generated_sql.strip()

            print(f"Generated SQL: {generated_sql}")

            # Execute the generated SQL
            exec_result = conn.execute(text(generated_sql))
            rows = exec_result.fetchall()
            columns = exec_result.keys()

            # Format results
            results = [dict(zip(columns, row)) for row in rows]

            return jsonify({
                "nl_query": nl_query,
                "generated_sql": generated_sql,
                "results": results
            })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)