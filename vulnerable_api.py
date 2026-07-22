import os
import subprocess
import sqlite3
import pickle
import yaml
from flask import Flask, request, jsonify

app = Flask(__name__)

# CWE-798: Hardcoded credentials
SECRET_KEY = "super_secret_key_12345"
DATABASE_URL = "postgresql://admin:P@ssw0rd123@prod-db.internal:5432/users"
AWS_ACCESS_KEY = "AKIAIOSFODNN7EXAMPLE"
AWS_SECRET_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"

@app.route('/query', methods=['POST'])
def unsafe_query():
    # CWE-89: SQL Injection
    user_input = request.json.get('search')
    conn = sqlite3.connect('app.db')
    cursor = conn.execute(f"SELECT * FROM products WHERE name LIKE '%{user_input}%'")
    return jsonify([dict(row) for row in cursor])

@app.route('/run', methods=['POST'])
def run_command():
    # CWE-78: OS Command Injection
    hostname = request.json.get('host')
    result = os.popen(f"ping -c 1 {hostname}").read()
    return jsonify({"output": result})

@app.route('/deserialize', methods=['POST'])
def unsafe_deserialize():
    # CWE-502: Deserialization of Untrusted Data
    data = request.get_data()
    obj = pickle.loads(data)
    return jsonify({"result": str(obj)})

@app.route('/config', methods=['POST'])
def load_config():
    # CWE-20: Improper Input Validation + unsafe YAML load
    config_data = request.get_data(as_text=True)
    config = yaml.load(config_data)  # unsafe yaml.load without Loader
    return jsonify(config)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
