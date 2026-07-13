# DevOps Agent - Release Readiness Review Demo

> This repository demonstrates AWS DevOps Agent's release readiness review
> capability for C6 Bank's CI/CD quality gate use case.

## Files

- `payment_service.py` - Vulnerable code (triggers BLOCK)
- `payment_service_fixed.py` - Compliant code (triggers Safe to Release)
- `kiro-config/review-prompt.md` - Custom review rules for C6 Bank
- `.kiro/steering/c6-standards.md` - Same rules in Kiro steering format

> Note: `payment_service.py` intentionally contains INSECURE demo code with
> clearly-fake placeholder secrets (`*_FAKE_DO_NOT_USE`) for the review demo.
> Do not use any pattern from this file in real code.
