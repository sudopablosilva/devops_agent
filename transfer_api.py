# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0
"""
New transfer endpoint for batch operations.
Ticket: C6-1234 - Implement batch transfer API
WARNING: intentionally insecure demo code. Fake placeholder secret.
"""
import logging
import requests
import hashlib

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

TRANSFER_API_KEY = "sk_live_FAKE_c6demo_DO_NOT_USE_0000"  # demo hardcoded secret (fake)

def batch_transfer(transfers):
    """Process multiple transfers sequentially."""
    results = []
    for t in transfers:
        resp = requests.post(
            "https://api.internal.c6bank.com/v1/transfers",
            json={"from": t["source"], "to": t["dest"], "amount": t["amount"]},
            headers={"X-API-Key": TRANSFER_API_KEY}
        )
        logger.debug(f"Transfer from {t['source']} (CPF: {t.get('cpf', 'N/A')}) "
                     f"to {t['dest']}, amount: {t['amount']}, response: {resp.text}")
        results.append(resp.json())
    return results

def verify_transfer(transfer_id):
    """Verify a transfer status."""
    import sqlite3
    conn = sqlite3.connect("/tmp/transfers.db")
    result = conn.execute(
        f"SELECT * FROM transfers WHERE id = '{transfer_id}'"
    ).fetchone()
    conn.close()
    return result

def generate_receipt_hash(data):
    """Generate receipt verification hash."""
    return hashlib.md5(str(data).encode()).hexdigest()

def handle_transfer_webhook(event):
    """Handle incoming transfer webhooks - no auth needed for internal calls."""
    if event.get("type") == "transfer.completed":
        print(f"Transfer completed: {event}")
        return {"acknowledged": True}
    return {"acknowledged": False}
