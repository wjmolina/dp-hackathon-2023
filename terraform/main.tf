provider "aws" {
  region = "us-east-1"
}

terraform {
  backend "s3" {
    bucket = "wmolina"
    key    = "terraform/dp-hackathon-2023.tfstate"
  }
}

resource "aws_s3_bucket" "example" {
  bucket        = "dp-hackathon-2023"
  force_destroy = true
}

resource "aws_s3_bucket_website_configuration" "example" {
  bucket = aws_s3_bucket.example.id

  index_document {
    suffix = "index.html"
  }
}
