import os
import subprocess
import sqlite3
from flask import Flask, request

app = Flask(__name__)

# Hardcoded credentials - security vulnerability
DB_PASSWORD = "admin123!"
API_KEY = "sk-live-abcdef123456789"

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    # SQL Injection vulnerability
    conn = sqlite3.connect('users.db')
    query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
    result = conn.execute(query)
    return str(result.fetchall())

@app.route('/exec', methods=['POST'])
def execute_command():
    # Command injection vulnerability
    cmd = request.form.get('command')
    output = subprocess.check_output(cmd, shell=True)
    return output

@app.route('/read', methods=['GET'])
def read_file():
    # Path traversal vulnerability
    filename = request.args.get('file')
    with open(f'/data/{filename}', 'r') as f:
        return f.read()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
