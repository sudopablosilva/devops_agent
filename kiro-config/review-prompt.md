# Release Readiness Review Standards - C6 Bank

## Security Standards (BLOCK if violated)
- No hardcoded secrets, API keys, or credentials in source code
- No SQL injection vulnerabilities (use parameterized queries)
- No weak cryptography (MD5, SHA1, DES, ECB mode)
- No SSRF or path traversal patterns
- All payment endpoints MUST call fraud validation service
- All data-mutation endpoints MUST have audit logging
- All public endpoints MUST have JWT authentication via @c6/auth-middleware

## Internal Library Compliance (WARN if violated)
- HTTP calls MUST use @c6/http-client (not raw requests/axios/fetch)
- Logging MUST use @c6/logger (not print/console.log/logging.basicConfig)
- Circuit breaker MUST use @c6/resilience (not manual retry logic)
- Crypto operations MUST use @c6/crypto (not raw cryptography libs)
- Event handling MUST use @c6/event-bus (not raw SNS/SQS)

## Performance Standards (WARN if violated)
- No N+1 query patterns (DynamoDB scan + per-item query)
- No unbounded pagination (scan without Limit)
- Batch operations MUST be async (asyncio.gather or concurrent.futures)

## Observability Standards (WARN if violated)
- New endpoints MUST have latency/error metrics
- Error handlers MUST use structured logging
- Critical operations MUST have distributed tracing

## Deployment Safety (BLOCK if violated)
- Breaking API changes MUST have versioning
- Data migrations MUST be backward-compatible
- High-risk changes MUST have feature flags

## Review Output
- Recommend: BLOCK, Proceed with Caution, or Safe to Release
- Provide confidence score (0.0-1.0)
- When confidence < 0.7, always recommend human review
