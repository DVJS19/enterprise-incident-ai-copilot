provider "aws" {
  region = var.aws_region
  default_tags {
    tags = {
      Project     = var.project_name
      Environment = var.environment
      Owner       = var.owner
      ManagedBy   = "terraform"
      Phase       = "phase-1"
    }
  }
}

locals { name_prefix = "${var.project_name}-${var.environment}" }

module "s3" {
  source      = "../../modules/s3"
  name_prefix = local.name_prefix
}

module "dynamodb" {
  source      = "../../modules/dynamodb"
  name_prefix = local.name_prefix
}

module "observability" {
  source                = "../../modules/observability"
  name_prefix           = local.name_prefix
  lambda_log_group_name = "/aws/lambda/${local.name_prefix}-ai-gateway"
  api_log_group_name    = "/aws/apigateway/${local.name_prefix}"
}

module "iam" {
  source                   = "../../modules/iam"
  name_prefix              = local.name_prefix
  incident_state_table_arn = module.dynamodb.incident_state_table_arn
  audit_log_table_arn      = module.dynamodb.audit_log_table_arn
  workflow_state_table_arn = module.dynamodb.workflow_state_table_arn
  kb_bucket_arn            = module.s3.knowledge_base_bucket_arn
  artifacts_bucket_arn     = module.s3.artifacts_bucket_arn
}

module "lambda" {
  source                    = "../../modules/lambda"
  name_prefix               = local.name_prefix
  runtime                   = var.lambda_runtime
  timeout                   = var.lambda_timeout
  memory_size               = var.lambda_memory_size
  lambda_role_arn           = module.iam.lambda_role_arn
  incident_state_table_name = module.dynamodb.incident_state_table_name
  audit_log_table_name      = module.dynamodb.audit_log_table_name
  workflow_state_table_name = module.dynamodb.workflow_state_table_name
  knowledge_base_bucket     = module.s3.knowledge_base_bucket_name
  artifacts_bucket          = module.s3.artifacts_bucket_name
  source_dir                = "${path.module}/../../../services/ai_gateway/src"
}

module "api_gateway" {
  source                   = "../../modules/api_gateway"
  name_prefix              = local.name_prefix
  lambda_function_name     = module.lambda.lambda_function_name
  lambda_invoke_arn        = module.lambda.lambda_invoke_arn
  api_access_log_group_arn = module.observability.api_access_log_group_arn
}
