resource "aws_dynamodb_table" "security_findings_table" {
    name = "SecurityFindings"
    billing_mode = "PAY_PER_REQUEST"
    hash_key = "ResourceId"

    attribute {
        name = "ResourceId"
        type = "S"
    }
}