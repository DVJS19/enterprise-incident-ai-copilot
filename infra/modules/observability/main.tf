data "aws_region" "current" {}

resource "aws_cloudwatch_log_group" "lambda" {
  name              = var.lambda_log_group_name
  retention_in_days = 14
}

resource "aws_cloudwatch_log_group" "api_access" {
  name              = var.api_log_group_name
  retention_in_days = 14
}

resource "aws_cloudwatch_dashboard" "main" {
  dashboard_name = "${var.name_prefix}-dashboard"
  dashboard_body = jsonencode({
    widgets = [
      {
        type = "metric", x = 0, y = 0, width = 12, height = 6,
        properties = {
          title  = "AI Gateway Lambda"
          region = data.aws_region.current.name
          metrics = [
            ["AWS/Lambda", "Invocations", "FunctionName", "${var.name_prefix}-ai-gateway"],
            [".", "Errors", ".", "."],
            [".", "Duration", ".", "."]
          ]
          stat = "Sum"
        }
      }
    ]
  })
}
