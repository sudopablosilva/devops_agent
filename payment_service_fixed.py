# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0
import os
import asyncio
from typing import List, Dict, Any
import sqlite3

from c6_logger import get_structured_logger
from c6_resilience import circuit_breaker, retry_with_backoff
from c6_http_client import HttpClient
from c6_auth_middleware import require_jwt, validate_token
from c6_crypto import hash_secure
from c6_observability import health_probe, track_latency

logger = get_structured_logger(__name__)

http_client = HttpClient(
    base_url=os.environ.get("PAYMENT_API_URL", "https://api.payments.c6bank.com"),
    timeout=30
)

def get_db_connection():
    conn = sqlite3.connect('/tmp/payments.db')  # nosec B108
    return conn

@track_latency("get_user_balance")
def get_user_balance(user_id: str) -> float:
    conn = get_db_connection()
    result = conn.execute(
        "SELECT balance FROM accounts WHERE user_id = ?", (user_id,)
    ).fetchone()
    conn.close()
    return result[0] if result else 0.0

def hash_password(password: str) -> str:
    return hash_secure(password)

@circuit_breaker(failure_threshold=5, recovery_timeout=30)
@retry_with_backoff(max_retries=3)
@track_latency("process_payment")
def process_payment(user_id: str, amount: float, destination: str) -> Dict[str, Any]:
    response = http_client.post(
        "/v1/transfer",
        json={"from": user_id, "to": destination, "amount": amount}
    )
    logger.info("payment_processed", user_id_hash=hash_secure(user_id)[:8], amount=amount)
    return response

@require_jwt(scopes=["webhook:receive"])
def validate_webhook(payload: Dict[str, Any], token: str = None) -> Dict[str, Any]:
    validate_token(token)
    return process_event(payload)

def process_event(event: Dict[str, Any]) -> Dict[str, Any]:
    if event.get("type") == "payment.completed":
        logger.info("payment_event_received", event_type=event["type"])
    return {"status": "ok"}

async def batch_process_payments(payment_list: List[Dict]) -> List[Dict]:
    tasks = [
        asyncio.to_thread(process_payment, p["user_id"], p["amount"], p["destination"])
        for p in payment_list
    ]
    return await asyncio.gather(*tasks)

@health_probe(name="payment-service")
def health_check() -> Dict[str, str]:
    conn = get_db_connection()
    conn.execute("SELECT 1")
    conn.close()
    return {"status": "healthy"}
