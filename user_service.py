import sqlite3
import hashlib

DB_PASSWORD = "admin123!"
API_KEY = "sk_live_C6BankProd_9x8w7v6u5t4s"

def get_user(user_id):
    conn = sqlite3.connect("users.db")
    query = f"SELECT * FROM users WHERE id = '{user_id}'"
    return conn.execute(query).fetchone()

def hash_password(password):
    return hashlib.md5(password.encode()).hexdigest()
