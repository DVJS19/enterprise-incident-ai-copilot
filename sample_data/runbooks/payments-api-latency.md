# Payments API Latency Runbook

## Symptoms
- p95 latency above 500ms
- DynamoDB throttling
- Increased checkout latency

## Diagnosis
1. Check recent deployments.
2. Check DynamoDB throttled requests.
3. Check cache status.
4. Compare with previous latency incidents.

## Mitigation
1. Re-enable payment-profile-cache.
2. Roll back the latest deployment if latency started after release.
3. Temporarily increase DynamoDB read capacity.
4. Notify payments-platform-team.

## Prevention
- Add load test for DynamoDB access pattern changes.
- Add deployment-aware latency alert.
- Keep cache configuration protected by approval.