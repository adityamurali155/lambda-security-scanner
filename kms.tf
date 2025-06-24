resource "aws_kms_key" "dynamodb_key" {
  description             = "KMS key for encrypting DynamoDB table"
  deletion_window_in_days = 10
  enable_key_rotation     = true

    policy = jsonencode({
    Version = "2012-10-17",
    Id      = "lambda-only-policy",
    Statement: [
      # Allow Lambda's IAM role full KMS access
      {
        Sid: "AllowLambdaUse",
        Effect: "Allow",
        Principal: {
          AWS: aws_iam_role.lambda_exec.arn
        },
        Action: [
          "kms:Encrypt",
          "kms:Decrypt",
          "kms:ReEncrypt*",
          "kms:GenerateDataKey*"
        ],
        Resource: "*"
      },
      # Allow the root user in the account to administer the key
      {
        Sid: "AllowRootAccountAdmin",
        Effect: "Allow",
        Principal: {
          AWS: "arn:aws:iam::${data.aws_caller_identity.current.account_id}:root"
        },
        Action: "kms:*",
        Resource: "*"
      }
    ]
  })
}
resource "aws_kms_alias" "dynamodb_key_alias" {
  name          = "alias/dynamodbKey"
  target_key_id = aws_kms_key.dynamodb_key.key_id
}
