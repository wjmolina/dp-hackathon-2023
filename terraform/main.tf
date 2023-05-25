provider "aws" {
  region = "us-east-1"
}

terraform {
  backend "s3" {
    bucket = "wmolina"
    key    = "terraform/dp-hackathon-2023.tfstate"
  }
}

resource "aws_s3_bucket" "example_bucket" {
  bucket = "dp-hackathon-2023"
  website {
    index_document = "index.html"
    error_document = "error.html"
  }
}
