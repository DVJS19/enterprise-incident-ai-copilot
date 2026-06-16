# Payments API Known Issues

## Issue: Latency after deployment

### Symptoms
- p95 latency above 500ms
- DynamoDB throttled requests
- Payment confirmation delays

### Known Cause
A deployment changed the DynamoDB access pattern and disabled payment-profile-cache.

### Recommended Fix
1. Re-enable payment-profile-cache.
2. Review or roll back the latest deployment.
3. Temporarily increase DynamoDB read capacity.
4. Monitor p95 latency and throttled requests.