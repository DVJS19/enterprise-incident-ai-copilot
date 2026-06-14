data "archive_file" "lambda_zip" {
  type        = "zip"
  source_dir  = var.source_dir
  output_path = "${path.module}/.build/${var.name_prefix}-ai-gateway.zip"
}

resource "aws_lambda_function" "ai_gateway" {
  function_name    = "${var.name_prefix}-ai-gateway"
  role             = var.lambda_role_arn
  handler          = "handler.lambda_handler"
  runtime          = var.runtime
  timeout          = var.timeout
  memory_size      = var.memory_size
  filename         = data.archive_file.lambda_zip.output_path
  source_code_hash = data.archive_file.lambda_zip.output_base64sha256

  environment {
    variables = {
      INCIDENT_STATE_TABLE  = var.incident_state_table_name
      AUDIT_LOG_TABLE       = var.audit_log_table_name
      WORKFLOW_STATE_TABLE  = var.workflow_state_table_name
      KNOWLEDGE_BASE_BUCKET = var.knowledge_base_bucket
      ARTIFACTS_BUCKET      = var.artifacts_bucket
      LOG_LEVEL             = "INFO"
    }
  }
}
