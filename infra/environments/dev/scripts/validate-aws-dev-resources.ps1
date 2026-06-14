param(
  [string]$Region = "us-west-2",
  [string]$ProjectName = "incident-ai-copilot",
  [string]$Environment = "dev"
)

$Prefix = "$ProjectName-$Environment"

Write-Host "`nChecking AWS resources for prefix: $Prefix in $Region`n"

function Check-Command($Name, $Command) {
  Write-Host "Checking $Name..."
  try {
    $result = Invoke-Expression $Command
    if ($LASTEXITCODE -eq 0 -and $result) {
      Write-Host "FOUND: $Name" -ForegroundColor Yellow
      $result
    } else {
      Write-Host "NOT FOUND: $Name" -ForegroundColor Green
    }
  }
  catch {
    Write-Host "NOT FOUND or ERROR: $Name" -ForegroundColor Green
  }
  Write-Host ""
}

Check-Command "S3 buckets" `
  "aws s3api list-buckets --query `"Buckets[?contains(Name, '$Prefix')].Name`" --output table"

Check-Command "DynamoDB tables" `
  "aws dynamodb list-tables --region $Region --query `"TableNames[?contains(@, '$Prefix')]`" --output table"

Check-Command "Lambda functions" `
  "aws lambda list-functions --region $Region --query `"Functions[?contains(FunctionName, '$Prefix')].FunctionName`" --output table"

Check-Command "API Gateway HTTP APIs" `
  "aws apigatewayv2 get-apis --region $Region --query `"Items[?contains(Name, '$Prefix')].[Name,ApiId]`" --output table"

Check-Command "CloudWatch Log Groups" `
  "aws logs describe-log-groups --region $Region --log-group-name-prefix `"/aws/lambda/$Prefix`" --query `"logGroups[].logGroupName`" --output table"

Check-Command "API Gateway Log Groups" `
  "aws logs describe-log-groups --region $Region --log-group-name-prefix `"/aws/apigateway/$Prefix`" --query `"logGroups[].logGroupName`" --output table"

Check-Command "IAM Roles" `
  "aws iam list-roles --query `"Roles[?contains(RoleName, '$Prefix')].RoleName`" --output table"

Check-Command "IAM Policies" `
  "aws iam list-policies --scope Local --query `"Policies[?contains(PolicyName, '$Prefix')].[PolicyName,Arn]`" --output table"

Check-Command "CloudWatch Dashboards" `
  "aws cloudwatch list-dashboards --region $Region --dashboard-name-prefix $Prefix --query `"DashboardEntries[].DashboardName`" --output table"

Write-Host "Validation complete."
Write-Host "After terraform destroy, all checks should return NOT FOUND or empty tables." -ForegroundColor Cyan