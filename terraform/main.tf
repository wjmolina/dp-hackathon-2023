provider "aws" {
  region = "us-east-1"
}

terraform {
  backend "s3" {
    bucket = "wmolina"
    key    = "terraform/dp-hackathon-2023.tfstate"
  }
}

resource "aws_s3_bucket" "static_website_bucket" {
  bucket = "dp-hackathon-2023"
  website {
    index_document = "index.html"
    error_document = "error.html"
  }
}

resource "aws_s3_bucket_policy" "static_website_bucket_policy" {
  bucket = aws_s3_bucket.static_website_bucket.id
  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "PublicReadGetObject",
      "Effect": "Allow",
      "Principal": "*",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::${aws_s3_bucket.static_website_bucket.id}/*"
    }
  ]
}
EOF
}

resource "aws_s3_bucket_public_access_block" "static_website_bucket_public_access_block" {
  bucket                  = aws_s3_bucket.static_website_bucket.id
  block_public_acls       = false
  block_public_policy     = false
  ignore_public_acls      = false
  restrict_public_buckets = false
}
