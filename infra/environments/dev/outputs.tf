output "api_endpoint" { value = module.api_gateway.api_endpoint }
output "incident_analyze_endpoint" { value = "${module.api_gateway.api_endpoint}/incident/analyze" }
output "lambda_function_name" { value = module.lambda.lambda_function_name }
output "knowledge_base_bucket_name" { value = module.s3.knowledge_base_bucket_name }
output "artifacts_bucket_name" { value = module.s3.artifacts_bucket_name }
output "incident_state_table_name" { value = module.dynamodb.incident_state_table_name }
output "audit_log_table_name" { value = module.dynamodb.audit_log_table_name }
output "workflow_state_table_name" { value = module.dynamodb.workflow_state_table_name }
