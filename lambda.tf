resource "aws_iam_role" "lambda_exec_role" {
  name = "lambda-security-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [{
      Effect = "Allow",
      Principal = {
        Service = "lambda.amazonaws.com"
      },
      Action = "sts:AssumeRole"
    }]
  })
}
resource "aws_iam_policy" "lambda_security_policy"{
    name = "lambda-security-policy"

    policy = jsonencode({
        Version = "2012-10-17",
        Statement = [
        {
            Effect = "Allow",
            Action = [
            "ec2:DescribeInstances",
            "ec2:DescribeSecurityGroups",
            "rds:DescribeDBInstances",
            "s3:GetBucket*",
            "s3:ListBucket",
            "dynamodb:PutItem",
            "sns:Publish",
            "kms:Encrypt",
            "kms:Decrypt",
            "kms:GenerateDataKey",
            "logs:CreateLogGroup",
            "logs:CreateLogStream",
            "logs:PutLogEvents"
            ],
            Resource = "*"
        }
        ]
    })
}
resource "aws_iam_role_policy_attachment" "lambda_security_policy_attachment" {
  policy_arn = aws_iam_policy.lambda_security_policy.arn
  role       = aws_iam_role.lambda_exec_role.name
}
resource "aws_lambda_function" "security_checker" {
  function_name    = "lambda_function"
  runtime          = "python3.12"
  handler          = "lambda_function.lambda_handler"
  role             = aws_iam_role.lambda_exec_role.arn
  filename         = "lambda/lambda_function.zip"
  source_code_hash = filebase64sha256("lambda/lambda_function.zip")

  environment {
    variables = {
      SNS_TOPIC_ARN = aws_sns_topic.security_alerts.id
    }

  }
}