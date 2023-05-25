provider "aws" {
  region = "us-east-1"
}

terraform {
  backend "s3" {
    bucket = "foo"
    key    = "bar/baz"
  }
}
