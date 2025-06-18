resource "aws_kms_key" "dynamodb_key" {
  description             = "KMS key for encrypting DynamoDB table"
  deletion_window_in_days = 10
  enable_key_rotation     = true
}
resource "aws_kms_alias" "dynamodb_key_alias" {
  name          = "alias/dynamodbKey"
  target_key_id = aws_kms_key.dynamodb_key.key_id
}
