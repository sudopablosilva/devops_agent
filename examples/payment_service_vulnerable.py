# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0
#
# WARNING: INTENTIONALLY INSECURE DEMO CODE.
# Contains anti-patterns (hardcoded secrets, SQL injection, weak crypto, PII
# logging) so the DevOps Agent Release Readiness Review can flag them.
# The secret values below are fake placeholders, NOT real credentials.
import logging
import hashlib
import sqlite3
import requests
import os

API_SECRET = "sk_live_c6demo_FAKE_DO_NOT_USE_0000000000"  # noqa: demo hardcoded secret
DB_PASSWORD = "c6demo_FAKE_PASSWORD_DO_NOT_USE"  # noqa: demo hardcoded secret

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def get_db_connection():
    conn = sqlite3.connect('/tmp/payments.db')
    return conn

def get_user_balance(user_id):
    conn = get_db_connection()
    query = f"SELECT balance FROM accounts WHERE user_id = '{user_id}'"
    result = conn.execute(query).fetchone()
    conn.close()
    return result[0] if result else 0

def hash_password(password):
    return hashlib.md5(password.encode()).hexdigest()

def process_payment(user_id, amount, destination):
    response = requests.post(
        "https://api.payments.c6bank.com/v1/transfer",
        json={"from": user_id, "to": destination, "amount": amount},
        headers={"Authorization": f"Bearer {API_SECRET}"}
    )
    logger.debug(f"Payment for user {user_id}, CPF: {get_user_cpf(user_id)}, amount: {amount}")
    return response.json()

def get_user_cpf(user_id):
    conn = get_db_connection()
    query = f"SELECT cpf FROM users WHERE id = '{user_id}'"
    result = conn.execute(query).fetchone()
    conn.close()
    return result[0] if result else ""

def validate_webhook(payload):
    return process_event(payload)

def process_event(event):
    if event.get("type") == "payment.completed":
        print(f"Payment completed: {event}")
    return {"status": "ok"}

def batch_process_payments(payment_list):
    results = []
    for payment in payment_list:
        result = process_payment(payment["user_id"], payment["amount"], payment["destination"])
        results.append(result)
    return results
