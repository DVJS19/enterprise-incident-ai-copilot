# Dev AWS Resource Validation

This folder contains an AWS CLI validation script for the Terraform resources in `infra/environments/dev`.

## Created Resources

The dev environment creates:

| Area | Resource | Name source |
| --- | --- | --- |
| S3 | Knowledge base bucket | `terraform output knowledge_base_bucket_name` |
| S3 | Artifacts bucket | `terraform output artifacts_bucket_name` |
| DynamoDB | Incident state table | `terraform output incident_state_table_name` |
| DynamoDB | Audit log table | `terraform output audit_log_table_name` |
| DynamoDB | Workflow state table | `terraform output workflow_state_table_name` |
| IAM | Lambda execution role | `<project>-<environment>-ai-gateway-role` |
| IAM | Lambda IAM policy | `<project>-<environment>-ai-gateway-policy` |
| Lambda | AI gateway function | `terraform output lambda_function_name` |
| API Gateway | HTTP API | `<project>-<environment>-api` |
| API Gateway | Route | `POST /incident/analyze` |
| CloudWatch Logs | Lambda log group | `/aws/lambda/<project>-<environment>-ai-gateway` |
| CloudWatch Logs | API access log group | `/aws/apigateway/<project>-<environment>` |
| CloudWatch | Dashboard | `<project>-<environment>-dashboard` |

For the current dev variables, `<project>-<environment>` is expected to be `incident-ai-copilot-dev`.

## Prerequisites

Install and configure:

- Terraform
- AWS CLI v2
- AWS credentials with read access to the deployed resources

Confirm your AWS identity:

```powershell
aws sts get-caller-identity --region us-west-2
```

Confirm Terraform has outputs from an applied state:

```powershell
cd infra/environments/dev
terraform output
```

## Run Validation

From the dev environment folder:

```powershell
cd infra/environments/dev
.\validate-resources\validate-aws-resources.ps1
```

Or run with explicit parameters:

```powershell
.\validate-resources\validate-aws-resources.ps1 -Region us-west-2 -TerraformDirectory .
```

The script exits with:

- `0` when all checks pass
- `1` when one or more checks fail

## What The Script Checks

The script validates:

- AWS credentials are active.
- Terraform outputs are available.
- Both S3 buckets exist.
- S3 bucket encryption is `AES256`.
- S3 bucket versioning is enabled.
- S3 public access block is enabled.
- Artifacts bucket has the temporary artifact lifecycle rule.
- All DynamoDB tables exist and are active.
- DynamoDB tables use `PAY_PER_REQUEST`.
- DynamoDB tables have `PK` and `SK` keys.
- DynamoDB TTL is enabled or enabling on the `ttl` attribute.
- Lambda exists with the expected runtime, timeout, memory, and environment variables.
- Lambda IAM role and policy exist, and the policy is attached.
- CloudWatch log groups exist with 14 day retention.
- CloudWatch dashboard exists.
- API Gateway HTTP API exists.
- API Gateway route `POST /incident/analyze` exists.
- API Gateway default stage exists and auto deploy is enabled.

## Useful Manual Commands

Read all Terraform outputs:

```powershell
terraform output
```

Check S3 buckets:

```powershell
aws s3api head-bucket --bucket $(terraform output -raw knowledge_base_bucket_name) --region us-west-2
aws s3api head-bucket --bucket $(terraform output -raw artifacts_bucket_name) --region us-west-2
```

Check DynamoDB tables:

```powershell
aws dynamodb describe-table --table-name $(terraform output -raw incident_state_table_name) --region us-west-2
aws dynamodb describe-table --table-name $(terraform output -raw audit_log_table_name) --region us-west-2
aws dynamodb describe-table --table-name $(terraform output -raw workflow_state_table_name) --region us-west-2
```

Check Lambda:

```powershell
aws lambda get-function-configuration --function-name $(terraform output -raw lambda_function_name) --region us-west-2
```

Check API Gateway:

```powershell
aws apigatewayv2 get-apis --region us-west-2
```

Check CloudWatch log groups:

```powershell
aws logs describe-log-groups --log-group-name-prefix /aws/lambda/incident-ai-copilot-dev-ai-gateway --region us-west-2
aws logs describe-log-groups --log-group-name-prefix /aws/apigateway/incident-ai-copilot-dev --region us-west-2
```

Check the dashboard:

```powershell
aws cloudwatch get-dashboard --dashboard-name incident-ai-copilot-dev-dashboard --region us-west-2
```

## Endpoint

Get the deployed API endpoint:

```powershell
terraform output -raw incident_analyze_endpoint
```

The endpoint is expected to accept:

```text
POST /incident/analyze
```
