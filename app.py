from flask import Flask, request, jsonify
import sqlite3
from datetime import datetime
import os

app = Flask(__name__)

# Get the database path from an environment variable, or use a default path
DATABASE_DIR = os.environ.get('DATABASE_DIR', '/app')
DATABASE_PATH = os.path.join(DATABASE_DIR, 'orders.db')

# Ensure that the 'orders_data' directory exists
if not os.path.exists(DATABASE_DIR):
    os.makedirs(DATABASE_DIR)

# Helper function to connect to the database
def get_db_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row  # This helps to return rows as dictionaries
    return conn

# Initialize the database (Create orders table if it doesn't exist)
def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            status TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Create a new order
@app.route('/orders', methods=['POST'])
def create_order():
    data = request.get_json()

    # Validate incoming data
    if not data or not data.get('product_id') or not data.get('quantity'):
        return jsonify({"error": "Product ID and quantity are required"}), 400

    # Insert the new order into the database
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        INSERT INTO orders (product_id, quantity, status, created_at)
        VALUES (?, ?, ?, ?)
    ''', (data['product_id'], data['quantity'], 'created', datetime.utcnow().isoformat()))
    conn.commit()
    order_id = cur.lastrowid
    conn.close()

    return jsonify({
        'order_id': order_id,
        'product_id': data['product_id'],
        'quantity': data['quantity'],
        'status': 'created',
        'created_at': datetime.utcnow().isoformat()
    }), 201

# Get details of a specific order
@app.route('/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    conn = get_db_connection()
    order = conn.execute('SELECT * FROM orders WHERE id = ?', (order_id,)).fetchone()
    conn.close()

    if order is None:
        return jsonify({"error": "Order not found"}), 404

    return jsonify({
        'order_id': order['id'],
        'product_id': order['product_id'],
        'quantity': order['quantity'],
        'status': order['status'],
        'created_at': order['created_at']
    })

# Update the status of an order
@app.route('/orders/<int:order_id>/status', methods=['PUT'])
def update_order_status(order_id):
    data = request.get_json()

    if not data or not data.get('status'):
        return jsonify({"error": "Status is required"}), 400

    conn = get_db_connection()
    order = conn.execute('SELECT * FROM orders WHERE id = ?', (order_id,)).fetchone()

    if order is None:
        conn.close()
        return jsonify({"error": "Order not found"}), 404

    conn.execute('UPDATE orders SET status = ? WHERE id = ?', (data['status'], order_id))
    conn.commit()
    conn.close()

    return jsonify({
        'order_id': order_id,
        'product_id': order['product_id'],
        'quantity': order['quantity'],
        'status': data['status'],
        'created_at': order['created_at']
    }), 200

# Run the app
if __name__ == '__main__':
    init_db()  # Ensure the database is initialized before running
    app.run(host='0.0.0.0', port=5000)
