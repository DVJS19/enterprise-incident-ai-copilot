output "incident_state_table_name" { value = aws_dynamodb_table.incident_state.name }
output "incident_state_table_arn" { value = aws_dynamodb_table.incident_state.arn }
output "audit_log_table_name" { value = aws_dynamodb_table.audit_log.name }
output "audit_log_table_arn" { value = aws_dynamodb_table.audit_log.arn }
output "workflow_state_table_name" { value = aws_dynamodb_table.workflow_state.name }
output "workflow_state_table_arn" { value = aws_dynamodb_table.workflow_state.arn }
