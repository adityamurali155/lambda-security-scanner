resource "aws_s3_bucket" "vulnerable"{
    bucket = "vulnerable-bucket-4431"
    
    tags = {
        Name = "Vulnerable Bucket"
    }
}
resource "aws_s3_bucket_public_access_block" "bad_s3" {
  bucket = aws_s3_bucket.vulnerable.id

  block_public_acls       = false
  block_public_policy     = false
  ignore_public_acls      = false
  restrict_public_buckets = false
}
