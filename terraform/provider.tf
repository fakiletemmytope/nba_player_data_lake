terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "5.83.1"
    }
  }
  required_version = ">= 0.12"
}


provider "aws" {
  region = "us-east-1"
}
