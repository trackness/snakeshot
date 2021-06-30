provider "aws" {
  region              = var.region
  allowed_account_ids = [var.account_id]

  default_tags {
    tags = {
      Application = var.app_name
      Owner       = var.owner
      Environment = var.environment
      Region      = var.region
      GitRepo     = var.repo
      ManagedBy   = "Terraform"
    }
  }
}
