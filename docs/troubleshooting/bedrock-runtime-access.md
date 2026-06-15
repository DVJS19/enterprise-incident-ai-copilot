# Bedrock Runtime Access Issue

Date: YYYY-MM-DD

Issue:
ValidationException: Operation not allowed

Observed:
- list-foundation-models works
- list-inference-profiles works
- Converse fails for model IDs and inference profile ARNs

AWS Support Case:
<case number>

Temporary Mitigation:
- MockBedrockClient used during development